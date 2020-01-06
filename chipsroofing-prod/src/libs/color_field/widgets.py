from django.forms import widgets
from .color import Color


class ColorWidget(widgets.MultiWidget):
    """ Виджет цвета """
    class Media:
        js = (
            'color_field/admin/js/color.js',
        )
        css = {
            'all': (
                'color_field/admin/css/color.css',
            )
        }

    def __init__(self, attrs=None):
        color_widget = widgets.TextInput(attrs={
            'type': 'color',
            'class': 'colorfield-preview input-small',
        })
        input_widget = widgets.TextInput(attrs={
            'max_length': 7,
            'placeholder': 'hex color',
            'class': 'colorfield-hex input-small',
            'pattern': '#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})',
        })
        _widgets = (color_widget, input_widget)
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if not value:
            return [None, None]
        elif isinstance(value, str):
            value = Color(value)

        if isinstance(value, Color):
            return [value.color, value.color]
        else:
            return value

    def format_output(self, rendered_widgets):
        return '&nbsp;'.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        _color, color = super().value_from_datadict(data, files, name)
        if not color:
            return None

        color_obj = Color(color)
        return color_obj.db_value


class ColorOpacityWidget(widgets.MultiWidget):
    """ Виджет цвета с прозрачностью """
    class Media:
        js = (
            'color_field/admin/js/color.js',
        )
        css = {
            'all': (
                'color_field/admin/css/color.css',
            )
        }

    def __init__(self, attrs=None):
        color_widget = widgets.TextInput(attrs={
            'type': 'color',
            'class': 'colorfield-preview input-small',
        })
        input_widget = widgets.TextInput(attrs={
            'max_length': 7,
            'placeholder': 'hex color',
            'class': 'colorfield-hex input-small',
            'pattern': '#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})',
        })
        opacity_widget = widgets.TextInput(attrs={
            'type': 'number',
            'placeholder': 'opacity',
            'class': 'colorfield-opacity input-mini',
            'step': '0.05',
            'min': 0,
            'max': 1,
        })
        _widgets = (color_widget, input_widget, opacity_widget)
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if not value:
            return [None, None, None]
        elif isinstance(value, str):
            value = Color(value)

        if isinstance(value, Color):
            return [value.color, value.color, value.opacity]
        else:
            return value

    def format_output(self, rendered_widgets):
        return '&nbsp;'.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        _color, color, opacity = super().value_from_datadict(data, files, name)
        if not color:
            return None

        color_obj = Color(color, opacity or '1')
        return color_obj.db_value
