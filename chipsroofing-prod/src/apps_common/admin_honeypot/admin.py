from django.contrib import admin
from .forms import HoneypotLoginForm


class HoneypotAdminSite(admin.AdminSite):
    login_form = HoneypotLoginForm

    def __init__(self, name='admin_honeypot'):
        super().__init__(name)

    def has_permission(self, request):
        return False

honeypot_site = HoneypotAdminSite()
