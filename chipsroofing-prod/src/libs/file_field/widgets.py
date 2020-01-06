import os
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class FileWidget(forms.ClearableFileInput):
    """ Виджет выбора файла """
    class Media:
        css = {
            'all': (
                'file_field/admin/css/file_widget.css',
            )
        }
        js = (
            'file_field/admin/js/file_widget.js',
        )

    def is_initial(self, value):
        return bool(value and hasattr(value, 'url'))

    def render(self, name, value, attrs=None):
        context = dict(
            value=value,
            input=super(forms.FileInput, self).render(name, value, attrs),
            for_label=attrs.get('id', ''),
            filename=os.path.basename(value.name) if value else '',
        )

        if self.is_initial(value) and not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            context['clear'] = forms.CheckboxInput().render(
                checkbox_name, False, attrs={
                    'id': checkbox_id
                }
            )

        return mark_safe(render_to_string('file_field/admin/widget.html', context))
