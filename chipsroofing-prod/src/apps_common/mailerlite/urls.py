from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^subscribe/$', views_ajax.SubscribeView.as_view(), name='ajax_subscribe'),

    url(r'^test/(?P<campaign_id>\d+)/$', views.preview_campaign, name='preview'),
    url(r'^test/(?P<campaign_id>\d+)/plain/$', views.preview_campaign_plain, name='preview_plain'),
]
