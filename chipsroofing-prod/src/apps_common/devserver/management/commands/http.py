from wsgiref.handlers import SimpleHandler
from django.core.servers.basehttp import WSGIRequestHandler


class SlimWSGIRequestHandler(WSGIRequestHandler):
    """
    Hides all requests that originate from either ``STATIC_URL`` or ``MEDIA_URL``
    as well as any request originating with a prefix included in
    ``DEVSERVER_IGNORED_PREFIXES``.
    """
    def handle(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():  # An error code has been sent, just exit
            return

        handler = SimpleHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self  # backpointer for logging
        handler.run(self.server.get_app())

