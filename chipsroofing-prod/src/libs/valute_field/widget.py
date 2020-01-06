from django.forms import widgets
from suit.widgets import EnclosedInput
from .valute import Valute
from .utils import get_formatter


class ValuteWidget(EnclosedInput, widgets.NumberInput):
    input_type = 'number'

    def __init__(self, *args, **kwargs):
        formatter = get_formatter()
        widget_kwargs = formatter.get('widget_attrs') or {}
        attrs = dict(kwargs, **widget_kwargs)
        super().__init__(*args, **attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        if isinstance(value, Valute):
            value = value.as_string()

        return super().render(name, value, attrs)

