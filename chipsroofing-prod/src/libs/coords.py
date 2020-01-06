from numbers import Number
from decimal import Decimal, localcontext, ROUND_HALF_UP, InvalidOperation

__all__ = ['Coords']


class Coords:
    """
        Класс, описывающий пару координат.
        Используется в google_maps.
    """
    __slots__ = ('_lat', '_lng')

    def __new__(cls, lat=None, lng=None):
        self = object.__new__(cls)
        self._lat = self._format_number(lat)
        self._lng = self._format_number(lng)
        return self

    def __getnewargs__(self, *args):
        return self._lat, self._lng

    @classmethod
    def _format_number(cls, number):
        if isinstance(number, (Number, str)):
            try:
                value = Decimal(number)
            except InvalidOperation:
                raise ValueError('Invalid coordinate format: %r' % number)
            else:
                with localcontext() as ctx:
                    ctx.prec = 13
                    ctx.rounding = ROUND_HALF_UP
                    return value + 0
        elif isinstance(number, Decimal):
            return number
        else:
            raise TypeError('Invalid coordinates type: %r' % number)

    @property
    def lat(self):
        return self._lat

    @property
    def lng(self):
        return self._lng

    def get_point(self, srid=4326):
        from django.contrib.gis.geos import Point
        return Point(float(self._lng), float(self._lat), srid=srid)

    def __iter__(self):
        return iter((self.lat, self.lng))

    def __repr__(self):
        return '{0}, {1}'.format(self.lat, self.lng)
