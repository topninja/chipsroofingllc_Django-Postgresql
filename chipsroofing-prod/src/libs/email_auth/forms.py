from django import forms
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

UserModel = get_user_model()


class AuthenticationForm(forms.Form):
    """ Форма авторизации """
    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    email = forms.EmailField(
        label=_('Login (email)'),
        widget=forms.EmailInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your email')
        }
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password')
        }
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                self.add_error('password', forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                ))
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'email_exists': _('This email address is already taken'),
    }

    email = forms.EmailField(
        label='Email (your login)',
        required=True,
        widget=forms.EmailInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your email'),
            'invalid': _('Email incorrect'),
        }
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        try:
            UserModel._default_manager.get(email__iexact=email)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
                params={'email': email},
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.username = 'user_%d' % user.id
            user.save()
        return user


class ChangeEmailForm(forms.ModelForm):
    """ Форма изменения email """
    error_messages = {
        'email_exists': _('This email address is already taken'),
    }

    email = forms.EmailField(
        label=_("Account Name (Email)"),
        widget=forms.EmailInput(attrs={
            'autofocus': True,
        }),
        error_messages={
            'required': _('Please enter your email'),
            'invalid': _('Email incorrect'),
        }
    )

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        query = models.Q(email__iexact=email)
        if self.instance and self.instance.pk:
            query &= ~models.Q(pk=self.instance.pk)

        try:
            UserModel._default_manager.get(query)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
                params={'email': email},
            )
        return email
