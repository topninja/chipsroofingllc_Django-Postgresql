import os
from binascii import crc32
from urllib.parse import urljoin
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from django.core.files.storage import FileSystemStorage

MULTIDOMAIN_MEDIA = tuple(
    host if host.endswith('/') else host + '/'
    for host in getattr(settings, 'MEDIA_URLS', ())
)


class MediaStorage(FileSystemStorage):
    """
        Файловое хранилище в папке media
    """
    def __init__(self, directory=''):
        location = None
        base_url = None
        self.directory = directory.strip(' /')
        if self.directory:
            location = os.path.join(settings.MEDIA_ROOT, self.directory)
            base_url = '%s%s/' % (settings.MEDIA_URL, self.directory)
        super().__init__(location, base_url)

    def set_directory(self, directory):
        """ Динамическое изменение директории """
        self.directory = directory.strip(' /')
        if self.directory:
            self.base_location = self.location = os.path.join(settings.MEDIA_ROOT, self.directory)
            self.base_url = '%s%s/' % (settings.MEDIA_URL, self.directory)
        else:
            raise ValueError('empty directory in MediaStorage')

    def url(self, name):
        if MULTIDOMAIN_MEDIA:
            index = crc32(name.encode()) % len(MULTIDOMAIN_MEDIA)
            base_url = '%s%s/' % (MULTIDOMAIN_MEDIA[index], self.directory)
            return urljoin(base_url, filepath_to_uri(name))
        else:
            return urljoin(self.base_url, filepath_to_uri(name))
