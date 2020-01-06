import xml
from urllib import parse, request, error
from django.utils.translation import get_language
from . import conf


def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(latitude), float(longitude),)


def get_static_map_url(longitude, latitude, zoom=None, width=None, height=None):
    """ Возвращает URL статичной карты Google """
    if not latitude or not longitude:
        longitude, latitude = conf.DEFAULT_MAP_CENTER

    point = _format_point(longitude, latitude)

    return conf.STATIC_MAP_URL + parse.urlencode(dict(
        center=point,
        size='%dx%d' % (
            width or conf.STATIC_MAP_WIDTH,
            height or conf.STATIC_MAP_HEIGHT,
        ),
        zoom=zoom or conf.STATIC_MAP_ZOOM,
        maptype='roadmap',
        language=get_language(),
        markers='color:red|label:G|%s' % point,
    ))


def get_external_map_url(longitude, latitude, zoom=14):
    """ Возвращает URL карты на сервисе Google """
    if not latitude or not longitude:
        longitude, latitude = conf.DEFAULT_MAP_CENTER

    point = _format_point(longitude, latitude)

    return conf.EXTERNAL_MAP_URL + parse.urlencode(dict(
        q='loc:%s' % point,
        t='r',
        hl=get_language(),
        z=zoom,
    ))


def geocode(address, timeout=5.0):
    """ Возвращает кортеж координат (longtitude, latitude,) по строке адреса """
    params = parse.urlencode({'sensor': False, 'address': address})
    try:
        response = request.urlopen(conf.GEOCODE_URL + params, timeout=timeout)
    except error.URLError:
        return None

    try:
        dom = xml.dom.minidom.parseString(response.read())
        location_elem = dom.getElementsByTagName('location')[0]
        lng = location_elem.getElementsByTagName('lng')[0]
        lat = location_elem.getElementsByTagName('lat')[0]
    except IndexError:
        return None

    return lng.firstChild.data, lat.firstChild.data
