from . import settings
from .dev_modules import MODULES


class DevServerMiddleware(object):
    @staticmethod
    def should_process(request):
        for path in settings.DEVSERVER_IGNORED_PREFIXES:
            if request.path_info.startswith(path):
                return False

        return True

    def process_request(self, request):
        # Set a sentinel value which process_response can use to abort when
        # another middleware app short-circuits processing:
        request._devserver_active = True
        if self.should_process(request):
            for mod in MODULES:
                mod.process_request(request)

    def process_template_response(self, request, response):
        if self.should_process(request):
            for mod in MODULES:
                mod.process_template_response(request, response)
        return response

    def process_exception(self, request, exception):
        if self.should_process(request):
            for mod in MODULES:
                mod.process_exception(request, exception)

    def process_response(self, request, response):
        # If this isn't set, it usually means that another middleware layer
        # has returned an HttpResponse and the following middleware won't see
        # the request. This happens most commonly with redirections - see
        # https://github.com/dcramer/django-devserver/issues/28 for details:
        if not getattr(request, "_devserver_active", False):
            return response

        if self.should_process(request):
            for mod in reversed(MODULES):
                mod.process_response(request, response)

        return response
