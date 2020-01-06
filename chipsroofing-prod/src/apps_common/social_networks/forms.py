from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import FeedPost
from . import conf


class FeedPostForm(forms.ModelForm):
    network = forms.ChoiceField(
        required=True,
        label=_('Social network'),
        choices=conf.ALLOWED_NETWORKS,
        initial=FeedPost._meta.get_field('network').default,
    )

    class Meta:
        model = FeedPost
        fields = '__all__'


class AutpostForm(forms.Form):
    networks = forms.MultipleChoiceField(
        required=True,
        label=_('Social networks'),
        choices=conf.ALLOWED_NETWORKS,
        initial=FeedPost._meta.get_field('network').default,
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            'required': _('Please select at least one social network'),
        }
    )

    text = forms.CharField(
        required=True,
        label=_('Text'),
        widget=forms.Textarea(attrs={
            'maxlength': conf.TEXT_MAX_LENGTH,
            'rows': 3,
        }),
        error_messages={
            'required': _('Please enter text'),
        }
    )
