from django.apps import apps
from django.core.management.commands.dumpdata import Command as DumpDataCommand


class Command(DumpDataCommand):
    """
        Алиас для команды
            pm dumpdata --natural-foreign
                        --use_base_manager
                        --exclude=contenttypes
                        --exclude=auth.Permission
                        --exclude=admin.logentry
    """
    def handle(self, *args, **options):
        # exclude unmanaged models
        exclude = set(options.get('exclude', ()))
        exclude.update(['contenttypes', 'auth.Permission', 'admin.logentry'])
        for model in apps.get_models():
            if not model._meta.managed:
                exclude.add('%s.%s' % (model._meta.app_label, model._meta.model_name))

        options['exclude'] = exclude
        options['use_base_manager'] = True
        options['use_natural_foreign_keys'] = True
        super().handle(*args, **options)

