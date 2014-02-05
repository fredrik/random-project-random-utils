import re
import hashlib

from rest_framework import serializers, renderers, parsers
from django.utils.encoding import force_unicode

from .serialization import AwesomeEncoder


class JSONRenderer(renderers.JSONRenderer):
    encoder_class = AwesomeEncoder

    def render(self, data, *args, **kwargs):
        if data:
            data = recursive_key_map(underscore_to_camelcase, data)
        return super(JSONRenderer, self).render(data, *args, **kwargs)


class JSONParser(parsers.JSONParser):
    def parse(self, *args, **kwargs):
        obj = super(JSONParser, self).parse(*args, **kwargs)
        return recursive_key_map(camelcase_to_underscore, obj)


def underscore_to_camelcase(word, lower_first=True):
    result = ''.join(char.capitalize() for char in word.split('_'))
    if lower_first:
        return result[0].lower() + result[1:]
    else:
        return result

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


# http://stackoverflow.com/a/1176023
def camelcase_to_underscore(word):
    s1 = _first_cap_re.sub(r'\1_\2', word)
    return _all_cap_re.sub(r'\1_\2', s1).lower()


def recursive_key_map(function, obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.iteritems():
            if isinstance(key, basestring):
                key = function(key)
            new_dict[key] = recursive_key_map(function, value)
        return new_dict
    if hasattr(obj, '__iter__'):
        return [recursive_key_map(function, value) for value in obj]
    else:
        return obj


class FieldRenameMixin(object):
    def get_field_key(self, field_name):
        field_name = super(FieldRenameMixin, self).get_field_key(field_name)
        rename = getattr(self.opts, 'rename', {})
        return rename.get(field_name, field_name)


class ExtraFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        self.extra = kwargs.pop('extra', True)
        super(ExtraFieldsMixin, self).__init__(*args, **kwargs)

    def get_fields(self):
        if self.extra:
            self.opts.fields += self.opts.extra
        return super(ExtraFieldsMixin, self).get_fields()


class WriteOnlyFieldsMixin(object):
    def to_native(self, obj):
        ret = self._dict_class()
        ret.fields = self._dict_class()
        ret.empty = obj is None

        for field_name, field in self.fields.items():
            if field_name in self.opts.write_only_fields:
                continue
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            value = field.field_to_native(obj, field_name)
            ret[key] = value
            ret.fields[key] = field
        return ret


class SerializerOptions(serializers.ModelSerializerOptions):
    """
    Meta class options for Serializer
    """
    def __init__(self, meta):
        super(SerializerOptions, self).__init__(meta)
        self.rename = getattr(meta, 'rename', {})
        self.extra = getattr(meta, 'extra', ())
        self.write_only_fields = getattr(meta, 'write_only_fields', ())


class ModelSerializer(FieldRenameMixin,
                      ExtraFieldsMixin,
                      WriteOnlyFieldsMixin,
                      serializers.ModelSerializer):
    _options_class = SerializerOptions
