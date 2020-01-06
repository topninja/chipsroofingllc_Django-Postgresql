from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^result/$', views.result, name='result'),
]
