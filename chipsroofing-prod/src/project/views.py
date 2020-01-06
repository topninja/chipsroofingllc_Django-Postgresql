from django.apps import apps
from django.utils import timezone
from django.views.i18n import javascript_catalog
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_control

last_modified_date = timezone.now()


@cache_control(public=True, max_age=7*24*3600)
@last_modified(lambda req, **kw: last_modified_date)
def cached_javascript_catalog(request, domain='djangojs', packages=None):
    """ Закэшированный каталог JS-перевода """
    if packages is None:
        app_configs = apps.get_app_configs()
        packages = set(app_config.name for app_config in app_configs)

    packages.add('django.conf')
    return javascript_catalog(request, domain, packages)
