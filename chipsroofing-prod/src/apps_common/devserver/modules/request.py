from datetime import datetime
from django.core.management.color import color_style
from . import DevServerModule

style = color_style()


class RequestModule(DevServerModule):
    """
        Вывод адреса запроса и статуса ответа
    """
    logger_name = 'status'

    def process_request(self, request):
        super().process_request(request)
        date = ' %s ' % datetime.now().strftime('%H:%m:%S')
        date = date.center(30, '=')
        self.logger.info(date, indent='', prefix='')
        self.logger.info('%s %s' % (request.method, request.get_full_path()), indent='', prefix='')

    def process_response(self, request, response):
        code = str(response.status_code)

        msg = str(code)

        # Utilize terminal colors, if available
        if code[0] == '2':
            # Put 2XX first, since it should be the common case
            msg = style.HTTP_SUCCESS(msg)
        elif code[0] == '1':
            msg = style.HTTP_INFO(msg)
        elif code == '304':
            msg = style.HTTP_NOT_MODIFIED(msg)
        elif code[0] == '3':
            msg = style.HTTP_REDIRECT(msg)
        elif code == '404':
            msg = style.HTTP_NOT_FOUND(msg)
        elif code[0] == '4':
            msg = style.HTTP_BAD_REQUEST(msg)
        else:
            # Any 5XX, or any other response
            msg = style.HTTP_SERVER_ERROR(msg)

        self.logger.info(msg)
        super().process_response(request, response)
