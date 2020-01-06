from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class BaseStdImageWidget(forms.FileInput):
    template = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    def get_template(self, attrs=None):
        return (attrs and attrs.get('template')) or self.template

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        # Переносим классы в родительский элемент
        classes = final_attrs.pop('class', '')

        context = dict(self.context, **{
            'name': name,
            'value': value,
            'classes': classes,
            'attrs': flatatt(final_attrs),
            'preview': getattr(value, self.context['preview_variation']['name'], None),
        })

        return mark_safe(render_to_string(self.get_template(attrs), context))


class StdImageWidget(BaseStdImageWidget):
    """
        Виджет для клиентской части
    """
    template = 'stdimage/client_widget.html'

    class Media:
        js = (
            'stdimage/js/stdimage.js',
        )
        css = {
            'all': (
                'stdimage/css/stdimage.css',
            )
        }


class StdImageAdminWidget(BaseStdImageWidget):
    template = 'stdimage/admin/widget.html'

    class Media:
        js = (
            'common/js/jquery.Jcrop.js',
            'common/js/cropdialog.js',
            'stdimage/admin/js/stdimage.js',
        )
        css = {
            'all': (
                'common/css/jcrop/jquery.Jcrop.css',
                'admin/css/cropdialog/cropdialog.css',
                'stdimage/admin/css/stdimage.css',
            )
        }

    @staticmethod
    def clear_checkbox_name(name):
        return name + '-delete'

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if not self.is_required and forms.CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False

        return (
            upload,
            data.get('%s-croparea' % name, None) or None
        )
