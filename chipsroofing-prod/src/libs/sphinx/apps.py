from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.sphinx'
    verbose_name = _('Sphinx')

    def ready(self):
        import inspect
        import importlib
        from django.apps import apps
        from .index import ALL_INDEXES, SphinxXMLIndex

        for appconf in apps.get_app_configs():
            try:
                indexes_module = importlib.import_module('%s.indexes' % appconf.name)
            except ImportError:
                continue

            for name, member in inspect.getmembers(indexes_module, inspect.isclass):
                if member is SphinxXMLIndex or not issubclass(member, SphinxXMLIndex):
                    continue

                if member.name in ALL_INDEXES:
                    raise LookupError("Sphinx index with name '%s' already exists" % member.name)
                else:
                    ALL_INDEXES[member.name] = member
