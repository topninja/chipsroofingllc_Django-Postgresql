from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^download/(?P<file_id>\d+)/$', views.download, name='download'),
]
