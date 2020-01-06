from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^filter/(?P<application>[\w.]+)/(?P<model_name>\w+)/$',
        view=views.autocomplete_filter,
        name='autocomplete_filter'
    ),

    url(r'^(?P<application>[\w.]+)/(?P<model_name>\w+)/(?P<name>[-\w]+)/$',
        view=views.autocomplete_widget,
        name='autocomplete_widget'
    ),
]
