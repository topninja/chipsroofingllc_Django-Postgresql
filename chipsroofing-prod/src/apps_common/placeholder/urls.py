from django.conf.urls import url
from django.views.decorators.cache import never_cache
from . import views_ajax


urlpatterns = [
    url(r'^ajax/$', never_cache(views_ajax.MiddlewareView.as_view()), name='ajax'),
    url(r'^ajax/(?P<name>\w+)/$', never_cache(views_ajax.MiddlewareView.as_view()), name='ajax_named'),
]
