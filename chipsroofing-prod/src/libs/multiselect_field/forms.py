from django import forms
from django.forms import widgets


class CheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    outer_html = '<ul{id_attr}>{content}</ul>'
    inner_html = '<li>{choice_value}{sub_widgets}</li>'


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    renderer = CheckboxFieldRenderer


class MultiSelectFormField(forms.TypedMultipleChoiceField):
    widget = CheckboxSelectMultiple

