import time
from django.utils.termcolors import colorize
from . import DevServerModule


class ProfileRenderModule(DevServerModule):
    """
        Вывод времени рендеринга страницы
    """
    logger_name = 'render'

    def process_request(self, request):
        super().process_request(request)
        request._dev_render_start = time.time()

    def process_template_response(self, request, response):
        super().process_template_response(request, response)
        request._dev_render_view = time.time()

    def process_response(self, request, response):
        start_time = getattr(request, '_dev_render_start', 0)
        view_time = getattr(request, '_dev_render_view', 0)
        end_time = time.time()

        if view_time:
            view_duration = view_time - start_time
            self.logger.info(
                colorize(
                    '{:.0f}ms'.format(view_duration * 1000),
                    fg='white'
                ),
                name='view'
            )

        render_duration = end_time - max(view_time, start_time)
        self.logger.info(
            colorize(
                '{:.0f}ms'.format(render_duration * 1000),
                fg='white'
            ),
            name='render'
        )
        super().process_response(request, response)
