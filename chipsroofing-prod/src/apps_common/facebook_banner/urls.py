from django.conf.urls import url
from . import views_ajax


urlpatterns = [
    url(r'^ajax/$', views_ajax.BannerView.as_view(), name='ajax_facebook_banner'),
]
