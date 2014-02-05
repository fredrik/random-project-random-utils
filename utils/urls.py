import re

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


# http://stackoverflow.com/a/2507447/1442289
def url_target_blank(text):
    return re.sub("<a([^>]+)(?<!target=)>", '<a target="_blank"\\1>', text)


def get_admin_url(model):
    """ Returns an admin url for the given `model`, linking to the model's
    change form.

    """
    content_type = ContentType.objects.get_for_model(model.__class__)
    return reverse("admin:%s_%s_change" % (
        content_type.app_label,
        content_type.model),
        args=(model.id,)
    )
