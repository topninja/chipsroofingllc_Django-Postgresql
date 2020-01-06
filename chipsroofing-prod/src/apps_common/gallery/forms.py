from django import forms
from libs.form_helper.forms import FormHelperMixin
from .models import GalleryItemBase, GalleryImageItem


class GalleryItemBaseForm(FormHelperMixin, forms.ModelForm):
    csrf_token = False

    class Meta:
        model = GalleryItemBase
        fields = (
            'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
            })
        }


class GalleryImageItemForm(FormHelperMixin, forms.ModelForm):
    csrf_token = False

    class Meta:
        model = GalleryImageItem
        fields = (
            'image_alt', 'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
            })
        }
