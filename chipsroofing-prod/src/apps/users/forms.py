from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm,
    PasswordResetForm as DefaultPasswordResetForm,
    SetPasswordForm as DefaultSetPasswordForm
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from libs.form_helper.forms import FormHelperMixin

UserModel = get_user_model()


class LoginForm(FormHelperMixin, AuthenticationForm):
    """ Форма авторизации """
    error_messages = {
        'invalid_login': _('Login or password incorrect'),
        'inactive': _('Account blocked'),
    }

    username = forms.CharField(
        label=_('Login'),
        max_length=30,
        widget=forms.TextInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your login')
        }
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password')
        }
    )


class RegisterForm(FormHelperMixin, UserCreationForm):
    """ Форма регистрации """
    error_messages = {
        'password_mismatch': _('The two passwords didn\'t match'),
    }

    username = forms.RegexField(
        label=_('Login'),
        min_length=3,
        max_length=30,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your login'),
            'unique': _('This login is already taken'),
            'invalid': _('Login must contain only letters, numbers ans symbols @+-_'),
            'min_length': _('Login must be at least %(limit_value)s characters long'),
            'max_length': _('Login should not be longer than %(limit_value)s characters'),
        }
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        error_messages={
            'required': _('Please enter your e-mail'),
            'unique': _('This e-mail address is already taken'),
            'invalid': _('E-mail incorrect'),
        }
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password'),
        }
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'),
        error_messages={
            'required': _('Please enter password confirmation'),
        }
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserModel._default_manager.get(username=username)
        except ObjectDoesNotExist:
            return username
        self.add_field_error('username', 'unique')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            UserModel._default_manager.get(email__iexact=email)
        except ObjectDoesNotExist:
            return email
        self.add_field_error('email', 'unique')


class PasswordResetForm(FormHelperMixin, DefaultPasswordResetForm):
    """ Форма сброса пароля. Указание e-mail """
    error_messages = {
        'unregistered_email': _('E-mail is not registered'),
    }

    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your e-mail'),
            'invalid': _('E-mail incorrect'),
        }
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            UserModel._default_manager.get(email__iexact=email)
        except ObjectDoesNotExist:
            self.add_field_error('email', 'unregistered_email')
        return email


class SetPasswordForm(FormHelperMixin, DefaultSetPasswordForm):
    """ Форма сброса пароля. Указание нового пароля """
    error_messages = {
        'password_mismatch': _('The two passwords didn\'t match'),
    }

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your password'),
        }
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter password confirmation'),
        }
    )
