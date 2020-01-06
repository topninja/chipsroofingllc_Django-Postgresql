import os
from zipfile import ZipFile
from urllib import request, error
from django.core.management import BaseCommand
from ... import conf


class Command(BaseCommand):
    """
        Обновление базы GeoCity
    """
    help = 'Update SxGeo base'

    def reporthook(self, blocknum, bs, size):
        bar_width = 20

        progress = (blocknum * bs) / size
        bar_filled = round(bar_width * progress)
        line = 'Uploading... [%s>%s] %s%%\r' % (
            '=' * bar_filled,
            ' ' * (bar_width - bar_filled),
            int(progress * 100)
        )
        self.stdout.write(line, ending='')

    def handle(self, *args, **options):
        try:
            filename, headers = request.urlretrieve(conf.DB_UPDATE_URL, reporthook=self.reporthook)
        except error.HTTPError as e:
            self.stdout.write(e)
            return

        with ZipFile(filename, 'r') as zf:
            zf.extract(conf.DB_NAME, os.path.dirname(conf.DB_PATH))
        self.stdout.write('\nDone')
