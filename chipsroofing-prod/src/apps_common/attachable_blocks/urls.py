from django.conf.urls import url
from . import views_ajax


urlpatterns = [
    url(
        r'^ajax/$', views_ajax.get_blocks, name='ajax'
    ),
]
