import os
import zipfile
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand, call_command, CommandError


class Command(BaseCommand):
    """
        Создание дампа данных в zip-архиве
    """
    args = '<output directory>'
    help = 'Creates ZIP-archive with media and database dump'

    def handle(self, *args, **options):
        date = datetime.now().date()

        backup_name = '{}.zip'.format(date.strftime('%Y_%m_%d'))
        if args:
            backup_dir = os.path.abspath(args[0])
        else:
            backup_dir = settings.BACKUP_ROOT

        if not os.path.exists(backup_dir):
            raise CommandError('output directory does not exists')

        backup_path = os.path.join(backup_dir, backup_name)

        with zipfile.ZipFile(backup_path, 'w') as ziph:
            for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                for file in files:
                    abspath = os.path.abspath(os.path.join(root, file))
                    relpath = os.path.relpath(abspath, settings.MEDIA_ROOT)
                    ziph.write(abspath, os.path.join('media', relpath))

            # db dump
            dump_path = os.path.join(settings.BASE_DIR, 'dump.json')
            call_command('dump', output=dump_path)
            ziph.write(dump_path, 'dump.json')

        os.unlink('dump.json')
        self.stdout.write('backup saved to "%s"' % backup_path)
