from django import forms


class PhoneWidget(forms.TextInput):
    input_type = 'tel'
