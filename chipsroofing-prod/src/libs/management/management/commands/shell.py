"""
    Добавлены доп. параметры для iPython, заглушающие мусорные строки.
    Добавлена автозагрузка модулей при старте
"""
from django.conf import settings
from django.core.management import BaseCommand

SHELL_IMPORTS = [
    ('django.db', ('models', )),
    ('django.apps', ('apps', )),
    ('django.conf', ('settings', )),
    ('django.contrib.contenttypes.models', ('ContentType', )),
]


class Command(BaseCommand):
    help = "Runs a Python interactive interpreter. Tries to use IPython, if it is available."
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('-i', '--imports',
            action='store_true',
            dest='show_imports',
            default=False,
            help='Show imports'
        )
        parser.add_argument('-p', '--plain',
            action='store_true',
            dest='plain',
            help='Tells Django to use plain Python, not IPython or bpython.'
        )

    def import_objects(self, verbose):
        import importlib
        from django.apps import apps
        from django.utils.termcolors import colorize

        imported_objects = {}
        imports = SHELL_IMPORTS.copy()

        for app in apps.get_apps():
            if not app.__file__.startswith(settings.BASE_DIR):
                continue

            app_models = apps.get_models(app)
            if not app_models:
                continue

            modules = {}
            for model in app_models:
                data = modules.setdefault(model.__module__, [])
                data.append(model.__name__)

            for module_name, models in modules.items():
                imports.append((module_name, models))

        if verbose:
            self.stdout.write('Autoload modules:\n')

        for module_name, parts in imports:
            module = importlib.import_module(module_name)
            if not parts:
                imported_objects[module_name] = module

                if verbose:
                    msg = '  import %s\n' % module_name
                    self.stdout.write(colorize(msg, fg='green'))
            else:
                for part in parts:
                    imported_objects[part] = getattr(module, part)

                if verbose:
                    msg = '  from %s import %s\n' % (module_name, ', '.join(parts))
                    self.stdout.write(colorize(msg, fg='green'))

        return imported_objects

    def handle(self, *args, **options):
        use_plain = options.get('plain', False)
        show_imports = options.get('show_imports', True)

        imported_objects = self.import_objects(show_imports)

        try:
            if use_plain:
                # Don't bother loading IPython, because the user wants plain Python.
                raise ImportError

            from IPython import start_ipython
        except ImportError:
            # Plain
            import code
            # Set up a dictionary to serve as the environment for the shell, so
            # that tab completion works on objects that are imported at runtime.
            # See ticket 5082.
            try:  # Try activating rlcompleter, because it's handy.
                import readline
            except ImportError:
                pass
            else:
                # We don't have to wrap the following import in a 'try', because
                # we already know 'readline' was imported successfully.
                import rlcompleter
                readline.set_completer(rlcompleter.Completer(imported_objects).complete)
                readline.parse_and_bind("tab:complete")

            code.interact(banner='', local=imported_objects)
        else:
            # IPython
            start_ipython(argv=['--no-banner', '--no-confirm-exit'], user_ns=imported_objects)
