from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^add/(?P<content_type_id>\d+)/$',
        view=views.add_related,
        name='add_related'
    ),
    url(
        r'^change/(?P<content_type_id>\d+)/(?P<pk>\d+)/$',
        view=views.change_related,
        name='change_related'
    ),
    url(
        r'^delete/(?P<content_type_id>\d+)/(?P<pk>\d+)/$',
        view=views.delete_related,
        name='delete_related'
    ),
]
