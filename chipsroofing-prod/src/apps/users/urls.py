from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^ajax/login/$', views_ajax.LoginView.as_view(), name='ajax_login'),
    url(r'^ajax/logout/$', views_ajax.LogoutView.as_view(), name='ajax_logout'),
    url(r'^ajax/register/$', views_ajax.RegisterView.as_view(), name='ajax_register'),
    url(r'^ajax/reset/$', views_ajax.PasswordResetView.as_view(), name='ajax_reset'),
    url(r'^ajax/reset-confirm/$', views_ajax.ResetConfirmView.as_view(), name='ajax_reset_confirm'),
    url(r'^ajax/avatar_upload/$', views_ajax.AvatarUploadView.as_view(), name='avatar_upload'),
    url(r'^ajax/avatar_crop/$', views_ajax.AvatarCropView.as_view(), name='avatar_crop'),
    url(r'^ajax/avatar_delete/$', views_ajax.AvatarRemoveView.as_view(), name='avatar_delete'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^reset/$', views.PasswordResetView.as_view(), name='reset'),
    url(r'^reset_done/$', views.ResetDoneView.as_view(), name='reset_done'),
    url(r'^reset_confirm/$', views.ResetConfirmView.as_view(), name='reset_self'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.ResetConfirmView.as_view(), name='reset_confirm'),
    url(r'^reset_complete/$', views.ResetCompleteView.as_view(), name='reset_complete'),
    url(r'^reset_password/$', views.ResetConfirmView.as_view(), name='reset_password'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile_self'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.ProfileView.as_view(), name='profile'),
]
