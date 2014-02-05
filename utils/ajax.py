from scores import logging
from django.http import (HttpResponseNotAllowed, HttpResponseForbidden,
                         HttpResponseBadRequest, HttpResponseServerError)
from django.conf import settings
from functools import wraps
import traceback
import json


def ajax_view(FormClass=None, method='POST', login_required=True,
                                    logger=logging.getLogger('ajax_decorator')):

    def decorator(view_func):
        def _ajax_view(request, *args, **kwargs):
            if request.method != method and method != 'REQUEST':
                return HttpResponseNotAllowed(permitted_methods=[method])

            if login_required and not request.user.is_authenticated():
                return HttpResponseForbidden(
                    json.dumps({'error': 'User must be authenticated!'}),
                    mimetype='application/json'
                    )

            if FormClass:
                f = FormClass(getattr(request, method))
                if not f.is_valid():
                    return FormErrorResponse(f)
                request.form = f

            try:
                return view_func(request, *args, **kwargs)
            except:
                logger.exception('ajax_view decorator caught an exception in view function: %s.', view_func.__name__)
                response_data = {
                    'result': 'Exception',
                    'error': 'server',
                }
                if settings.DEBUG:
                    response_data['traceback'] = traceback.format_exc()
                return HttpResponseServerError(
                    json.dumps(response_data),
                    mimetype='application/json'
                    )
        return wraps(view_func)(_ajax_view)
    return decorator


def FormErrorResponse(form):
    return HttpResponseBadRequest(
        json.dumps({'result': 'Error', 'error': 'form', 'errors': form.errors}),
        mimetype='application/json'
        )
