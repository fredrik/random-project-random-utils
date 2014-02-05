from django.db.models import signals as model_signals
from utils.serialize import ModelSerializer


def dict_diff(old, new):
    """
    Return dictionary containing key:values from `new` that differ from `old`.
    """
    return {key: value
            for key, value in new.iteritems()
            if value != old[key]}


class CRUDHandler(object):
    """
    Object that abstracts registering of actions to be triggered by
    CRUD changes on models.

    on_* methods should be overriden to specify behavior.

    model:
        Django model to listen for events on.
    Serializer:
        Optional Serializer class to use for serialization of model when
        calculating diffs.
    """
    def __init__(self, model, Serializer=None, predicate=None):
        self.model = model
        self.Serializer = Serializer
        if predicate is not None:
            self.predicate = predicate

    def predicate(self, instance):
        """Decide whether a certain instance should be handled"""
        return True

    def on_create(self, instance):
        """Called on model creation."""
        pass

    def on_update(self, instance):
        """Called on model update."""
        pass

    def on_delete(self, instance):
        """Called on model deletion."""
        pass

    def on_all(self, instance):
        """Called on any CRUD action."""
        pass

    def register(self):
        """
        Register all handler signals.
        """
        model = self.model

        self._reset()

        # Set up pre-save signal handler to record changed fields.
        model_signals.pre_save.connect(self._model_diff_persist, sender=model,
                                       weak=False)

        # Set up post-save and post-delete signal handlers.
        model_signals.post_save.connect(self._post_save, sender=model,
                                        weak=False)
        model_signals.post_delete.connect(self._post_delete, sender=model,
                                          weak=False)

    def serialize(self, instance, *args, **kwargs):
        Serializer = self.get_serializer(instance)
        return Serializer(instance, *args, **kwargs)

    def get_serializer(self, model):
        """
        Returns Serializer class to use for serialization of given model
        when calculating diffs.
        """
        if self.Serializer:
            return self.Serializer
        class Serializer(ModelSerializer):
            class Meta:
                model = self.model
        return Serializer

    def _model_diff_persist(self, sender, instance, **kwargs):
        """
        Store information about the changes made to the model.

        To be called as a pre_save signal handler.
        """
        if not self.predicate(instance):
            return

        model = sender

        try:
            original = model._default_manager.get(pk=instance.pk)
        except model.DoesNotExist:
            # this is not an update, there is no original and no diff.
            return

        original_dict = self.serialize(original).data
        new_dict = self.serialize(instance).data
        changes = dict_diff(original_dict, new_dict)

        self.info['original'] = original_dict
        self.info['changes'] = changes

    def _reset(self):
        self.info = {
            'original': {},
            'changes': {},
        }

    def _post_save(self, sender, instance, created, **kwargs):
        """
        Forward post_save signal to relevant on_* method.
        """
        if not self.predicate(instance):
            return
        if created:
            self.on_create(instance)
        else:
            self.on_update(instance)
        self.on_all(instance)
        self._reset()

    def _post_delete(self, sender, instance, **kwargs):
        """
        Forward post_delete signal.
        """
        if not self.predicate(instance):
            return
        self.on_delete(instance)
        self.on_all(instance)
        self._reset()
