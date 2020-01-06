from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TestimonialsView.as_view(), name='index'),
]