from django import forms
from django.utils.encoding import smart_text
from .widgets import CKEditorWidget, CKEditorUploadWidget


class CKEditorFormField(forms.CharField):
    widget = CKEditorWidget

    def __init__(self, max_length=None, **kwargs):
        editor_options = kwargs.pop('editor_options')
        super().__init__(**kwargs)
        self.widget.editor_options = editor_options


class CKEditorUploadFormField(forms.Field):
    widget = CKEditorUploadWidget

    def __init__(self, max_length=None, **kwargs):
        editor_options = kwargs.pop('editor_options')
        upload_pagephoto_url = kwargs.pop('upload_pagephoto_url')
        upload_pagefile_url = kwargs.pop('upload_pagefile_url')
        upload_simplephoto_url = kwargs.pop('upload_simplephoto_url')
        model = kwargs.pop('model')
        super().__init__(**kwargs)
        self.widget.editor_options = editor_options
        self.widget.upload_pagephoto_url = upload_pagephoto_url
        self.widget.upload_pagefile_url = upload_pagefile_url
        self.widget.upload_simplephoto_url = upload_simplephoto_url
        self.widget.model = model

    def to_python(self, value):
        if isinstance(value, list):
            value[0] = smart_text(value[0])
        return value

    def clean(self, value):
        text, page_photos, page_files, simple_photos = value
        return super().clean(text), page_photos, page_files, simple_photos

    def has_changed(self, initial, data):
        data, *other = data
        return super().has_changed(initial, data)
