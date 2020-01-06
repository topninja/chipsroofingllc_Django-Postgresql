from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.form_helper.forms import FormHelperMixin
from libs.widgets import PhoneWidget
from .models import Message


class ContactForm(FormHelperMixin, forms.ModelForm):
    default_field_template = 'form_helper/unlabeled_field.html'

    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'type': forms.Select(attrs={
                'placeholder': _('Type'),
            }),
            'name': forms.TextInput(attrs={
                'placeholder': _('Name'),
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('E-mail'),
            }),
            'phone': PhoneWidget(attrs={
                'placeholder': _('Phone'),
            }),
            'message': forms.Textarea(attrs={
                'placeholder': _('Message'),
                'rows': 5,
            })
        }
        error_messages = {
            'name': {
                'required': _('Please enter your name'),
                'max_length': _('Name should not be longer than %(limit_value)d characters'),
            },
            'phone': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
            },
            'email': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('E-mail should not be longer than %(limit_value)d characters'),
            },
            'message': {
                'required': _('Please enter your message'),
                'max_length': _('Message should not be longer than %(limit_value)d characters'),
            },
        }

    def clean(self):
        """ Требуем указать email ИЛИ телефон """
        if 'phone' in self.cleaned_data and 'email' in self.cleaned_data:
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')

            if not phone and not email:
                self.add_field_error('phone', 'required')
                self.add_field_error('email', 'required')

        return super().clean()




class FreeEstimateForm(FormHelperMixin, forms.ModelForm):
    default_field_template = 'form_helper/unlabeled_field.html'

    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'type': forms.Select(attrs={
                'placeholder': _('Type'),
            }),
            'name': forms.TextInput(attrs={
                'placeholder': _('Name'),
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('E-mail'),
            }),
            'phone': PhoneWidget(attrs={
                'placeholder': _('Phone'),
            }),
            'message': forms.Textarea(attrs={
                'placeholder': _('Message'),
                'rows': 5,
            })
        }
        error_messages = {
            'name': {
                'required': _('Please enter your name'),
                'max_length': _('Name should not be longer than %(limit_value)d characters'),
            },
            'phone': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
            },
            'email': {
                'required': _('Please enter your e-mail or phone so we can contact you'),
                'max_length': _('E-mail should not be longer than %(limit_value)d characters'),
            },
            'message': {
                'required': _('Please enter your message'),
                'max_length': _('Message should not be longer than %(limit_value)d characters'),
            },
        }

    def clean(self):
        """ Требуем указать email ИЛИ телефон """
        if 'phone' in self.cleaned_data and 'email' in self.cleaned_data:
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')

            if not phone and not email:
                self.add_field_error('phone', 'required')
                self.add_field_error('email', 'required')

        return super().clean()
