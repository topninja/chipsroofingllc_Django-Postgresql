from ..logger import ThreadedConsoleHandler, ThreadedConsoleLogger


class DevServerModule(object):
    """
    Functions a lot like middleware, except that it does not accept any return values.
    """
    logger_name = 'devserver'

    def __init__(self):
        logger = ThreadedConsoleLogger(self.logger_name)
        logger.propagate = False
        handler = ThreadedConsoleHandler()
        logger.addHandler(handler)
        self.logger = logger

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_template_response(self, request, response):
        pass

    def process_response(self, request, response):
        self.logger.flush()

    def process_exception(self, request, exception):
        pass
