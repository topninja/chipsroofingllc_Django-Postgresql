from django.conf.urls import url
from . import views, views_ajax

urlpatterns = [
    url(r'^$', views.ExamplesView.as_view(), name='index'),
    url(r'^ajax/$', views_ajax.ExamplesView.as_view(), name='ajax_examples'),

]