from django.conf import settings

DEVSERVER_MODULES = getattr(settings, 'DEVSERVER_MODULES', (
    'devserver.modules.render.ProfileRenderModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.request.RequestModule',
))

DEVSERVER_IGNORED_PREFIXES = getattr(settings, 'DEVSERVER_IGNORED_PREFIXES', (
    settings.STATIC_URL,
    settings.MEDIA_URL,
    '/favicon',
    '/jsi18n',
))
