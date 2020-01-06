from django.conf.urls import url
from . import views_ajax

urlpatterns = [
    url(r'^vote/$', views_ajax.VoteView.as_view(), name='vote'),
]
