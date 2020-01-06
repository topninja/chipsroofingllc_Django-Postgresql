from django.conf.urls import url
from . import views, views_ajax
from .decorator import check_recaptcha


urlpatterns = [
    url(r'^ajax/$', check_recaptcha(views_ajax.ContactView.as_view()), name='ajax_contact'),

    url(r'^ajax/free_estimate/$', check_recaptcha(views_ajax.FreeEstimateView.as_view()), name='ajax_free_estimate'),

    url(r'^$', views.IndexView.as_view(), name='index'),
]
