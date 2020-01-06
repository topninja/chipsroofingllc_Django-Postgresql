import re
from decimal import Decimal, getcontext

re_hexcolor = re.compile('^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$')


class Color:
    __slots__ = ('_color', '_opacity', '_int_color')

    def __new__(cls, color, opacity='1'):
        self = object.__new__(cls)

        if isinstance(color, str) and ':' in color:
            color, opacity = color.split(':')

        self.color = color
        self.opacity = opacity
        return self

    def __getnewargs__(self, *args):
        return self._color, self._opacity

    def __str__(self):
        if self._opacity == 1:
            return self.color
        else:
            return self.rgba

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self._color, self._opacity)

    def __eq__(self, other):
        if isinstance(other, str):
            return self._opacity == Decimal(1) and self.color.lower() == other.lower()
        return super().__eq__(other)

    @property
    def opacity(self):
        opacity = str(self._opacity).rstrip('0').rstrip('.')
        return opacity if opacity else '0'

    @opacity.setter
    def opacity(self, value):
        try:
            cleaned_opacity = Decimal(value)
        except (TypeError, ValueError):
            raise ValueError('Invalid opacity')

        if cleaned_opacity < 0:
            cleaned_opacity = Decimal()
        elif cleaned_opacity > 1:
            cleaned_opacity = Decimal(1)
        context = getcontext().copy()
        context.prec = 3
        self._opacity = cleaned_opacity.quantize(Decimal('0.01'), context=context)

    @property
    def color(self):
        return '#%s' % self._color

    @color.setter
    def color(self, value):
        color_match = re_hexcolor.match(str(value))
        if not color_match:
            raise ValueError('Invalid color value')

        no_hash_color = color_match.group(1)
        if len(no_hash_color) == 3:
            cleaned_color = ''.join(letter * 2 for letter in no_hash_color).upper()
        else:
            cleaned_color = no_hash_color.upper()

        self._color = cleaned_color
        self._int_color = tuple(
            int(cleaned_color[i:i+2], 16)
            for i in range(0, len(cleaned_color), 2)
        )

    @property
    def rgb(self):
        return 'rgb({0}, {1}, {2})'.format(*self._int_color)

    @property
    def rgba(self):
        return 'rgba({1}, {2}, {3}, {0})'.format(self.opacity, *self._int_color)

    @property
    def db_value(self):
        if self._opacity == 1:
            return self._color
        else:
            return '{}:{}'.format(self._color, self._opacity)
