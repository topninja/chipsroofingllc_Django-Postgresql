from django.template import Library
from ..api import get_static_map_url, get_external_map_url
from ..models import geocode_cached

register = Library()


@register.filter(is_safe=True)
def google_map_static(address, params=None):
    """
    Фильтр, который возвращает URL картинки с картой.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру GoogleCoords

    Параметры:
        уровень детализации, ширина, высота - через запятую.

    Пример:

        <img src='{{ address|google_map_static:"15,300,200" }}'>
    """
    if not address:
        return ''

    if params is None:
        params = []
    else:
        params = [int(param.strip()) for param in params.split(",")]

    lng, lat = geocode_cached(address)
    return get_static_map_url(lng, lat, *params)


@register.filter(is_safe=True)
def google_map_external(address, zoom=14):
    """
    Фильтр, который возвращает URL карты у яндекса.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру GoogleCoords

    Принимает 1 необязательный параметр: уровень детализации.

    Пример:

        <a href='{{ address|google_map_external:15 }}' target='_blank'>посмотреть карту</a>
    """
    if not address:
        return ''

    lng, lat = geocode_cached(address)
    return get_external_map_url(lng, lat, zoom)
