from pysyge.pysyge import GeoLocator, MODE_BATCH, MODE_MEMORY
from . import conf


def info(ip, detailed=False):
    """
        Получение информации о IP.

        Пример:
            >>> info('8.8.8.8')
            {'region': None,
             'country': {'lon': -98.5,
              'iso': 'US',
              'lat': 39.76,
              'name_en': 'United States',
              'name_ru': 'США',
              'id': 225},
             'city': {'lat': 39.76,
              'name_en': True,
              'lon': -98.5,
              'name_ru': True,
              'id': 0}}

    """
    geodata = GeoLocator(conf.DB_PATH, MODE_BATCH | MODE_MEMORY)
    data = geodata.get_location(ip, detailed)
    return data.get('info') if data else data
