from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^set/(?P<code>[-\w]{2,5})/$', views.redirect_to_language, name='set_language'),
]
