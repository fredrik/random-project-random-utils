from django.conf.urls import url
from django.contrib.auth.views import login_required as login_required_decorator
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login_required(regex, view, *args, **kwargs):
    return url(regex, login_required_decorator(view), *args, **kwargs)


def view_by_auth(authed, not_authed):
    def view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return authed(request, *args, **kwargs)
        else:
            return not_authed(request, *args, **kwargs)
    return view


def view_by_tour(non_tour_view):
    def view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated() and not user.flags.get('shown_webapp_tour'):
            return HttpResponseRedirect(reverse('tour'))
        else:
            return non_tour_view(request, *args, **kwargs)
    return view


def base_url():
    current_site = Site.objects.get_current()
    return 'https://' + current_site.domain
