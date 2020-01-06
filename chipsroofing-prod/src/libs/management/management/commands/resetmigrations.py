import os
import shutil
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.core.management.base import CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('app_label', nargs='*', help='Applications')

    @staticmethod
    def get_resetable_apps(app_labels=()):
        """ Список приложений, чьи миграции нужно сбросить """
        local_apps = {}
        for app in apps.get_apps():
            app_path = apps._get_app_path(app)
            if app_path.startswith(settings.BASE_DIR):
                app_name = app.__name__.rsplit('.', 1)[0]
                local_apps[app_name] = app_path

        if app_labels:
            result_apps = {}
            for app_label in app_labels:
                if app_label in local_apps:
                    result_apps[app_label] = local_apps[app_label]
                else:
                    raise CommandError('application %s not found' % app_label)
            else:
                return result_apps
        else:
            return local_apps

    def handle(self, *args, **options):
        resetable_apps = self.get_resetable_apps(options['app_label'])

        # Удаление миграций
        for name, path in resetable_apps.items():
            migrations_dir = os.path.join(path, 'migrations')
            if os.path.isdir(migrations_dir):
                shutil.rmtree(migrations_dir)

        # Создание новых миграций
        for name, path in resetable_apps.items():
            self.stdout.write('Create migrations for %s...' % name)
            call_command('makemigrations', name.rsplit('.', 1)[-1], verbosity=0)

        call_command('migrate', verbosity=0)
