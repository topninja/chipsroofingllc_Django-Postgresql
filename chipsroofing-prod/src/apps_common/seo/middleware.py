from django import http
from django.conf import settings
from django.utils.timezone import now
from .models import Redirect


class RedirectMiddleware(object):
    @staticmethod
    def process_response(request, response):
        if response.status_code != 404:
            return response

        full_path = request.get_full_path()

        redirect = None
        try:
            redirect = Redirect.objects.get(old_path=full_path)
        except Redirect.DoesNotExist:
            pass

        if settings.APPEND_SLASH and not request.path.endswith('/'):
            # Try appending a trailing slash.
            path_len = len(request.path)
            full_path = full_path[:path_len] + '/' + full_path[path_len:]
            try:
                redirect = Redirect.objects.get(old_path=full_path)
            except Redirect.DoesNotExist:
                pass

        if redirect is None:
            return response

        if redirect.new_path == '':
            return http.HttpResponseGone()

        redirect.last_usage = now()
        redirect.save()

        if redirect.permanent:
            return http.HttpResponsePermanentRedirect(redirect.new_path)
        else:
            return http.HttpResponseRedirect(redirect.new_path)
