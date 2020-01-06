import inspect
import importlib
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
        Команда, запускающая скрипт на Python в окружении Django.

        В качестве пути к скрипту указывается:
            1) имя файла, если он лежит по-соседству с manage.py:
                "pm run do_something"
                -- запустит файл "do_something.py"
            2) Python-путь к модулю:
                "pm run application.scripts.do_something"

        Точкой входа в скрипте служит сам модуль или функция run(), если она определена.
        Точку входа можно переопределить параметром entry.
    """
    def add_arguments(self, parser):
        parser.add_argument('script')
        parser.add_argument('-e', '--entry', nargs='?', type=str, action='store', dest='entry', default='run')
        parser.add_argument(nargs='*', type=str, dest='script_params')

    def handle(self, *args, **options):
        script_args = []
        script_kwargs = {}
        for param in options.get('script_params', ()):
            if '=' in param:
                name, value = param.split('=', 1)
                script_kwargs[name] = value
            else:
                script_args.append(param)
        
        try:
            script = importlib.import_module(options['script'])
        except ImportError:
            print("No (valid) module for script '%s' found" % options['script'])
        else:
            run_func = getattr(script, options['entry'], None)
            if run_func and inspect.isfunction(run_func):
                run_func(*script_args, **script_kwargs)
