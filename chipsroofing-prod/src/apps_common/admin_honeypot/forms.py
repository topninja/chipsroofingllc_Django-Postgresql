from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm


class HoneypotLoginForm(AdminAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={
                    'username': self.username_field.verbose_name
                },
            )

        return self.cleaned_data
