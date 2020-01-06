from django import forms
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.encoding import force_text


class SpriteImageWidget(forms.Widget):
    """ Виджет выбора картинки из спрайта """
    template = 'sprite_image/admin/widget.html'

    class Media:
        css = {
            'all': (
                'sprite_image/admin/css/sprite_image.css',
            )
        }
        js = (
            'sprite_image/admin/js/sprite_image.js',
        )

    def __init__(self, *args, sprite='', size=(), background='#FFFFFF', **kwargs):
        self.sprite = sprite
        self.size = size
        self.background = background
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        text_value = force_text(value)
        final_attrs = self.build_attrs(attrs, name=name)
        if text_value != '':
            final_attrs['value'] = text_value

        choices = tuple(self.choices)
        choices_dict = dict(choices)

        return render_to_string(self.template, {
            'widget': self,
            'attrs': flatatt(final_attrs),
            'value': text_value,
            'choices': choices,
            'initial_position': choices_dict.get(text_value, (0, 0)),
        })
