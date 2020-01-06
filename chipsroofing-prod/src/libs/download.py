import os
import mimetypes
from urllib.parse import quote
from django.core.files.base import File
from django.http.response import FileResponse


class AttachmentResponse(FileResponse):
    """
        Response, заставляющий браузер скачать файл.

        Пример:
            # views.py
            def download(request, file_id):
                page_file = get_object_or_404(PageFile, pk=file_id)
                return AttachmentResponse(request, page_file.file)
    """
    block_size = 128 * 1024

    def __init__(self, request, stream, filename=None, *args, **kwargs):
        if isinstance(stream, str):
            stream = open(stream, 'rb')

        super().__init__(streaming_content=stream, *args, **kwargs)

        # filename
        if filename is None:
            if hasattr(stream, 'name'):
                filename = os.path.basename(stream.name)
            else:
                filename = 'file'

        # size
        if isinstance(stream, File):
            self['Content-Length'] = stream.size
        elif hasattr(stream, 'name'):
            self['Content-Length'] = os.path.getsize(stream.name)

        type_name, encoding = mimetypes.guess_type(filename)
        if type_name is None:
            type_name = 'application/octet-stream'
        self['Content-Type'] = type_name
        if encoding is not None:
            self['Content-Encoding'] = encoding

        # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
        if 'HTTP_USER_AGENT' in request.META and 'MSIE' in request.META['HTTP_USER_AGENT']:
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL, so we do the trick via routing rules.
            filename_header = ''
        else:
            # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
            filename_header = 'filename*=UTF-8\'\'%s' % quote(filename)

        self['Content-Disposition'] = 'attachment; ' + filename_header
