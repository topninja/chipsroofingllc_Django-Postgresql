import os
from django.conf import settings

DB_NAME = 'SxGeoCity.dat'
DB_PATH = os.path.abspath(os.path.join(settings.MEDIA_ROOT, DB_NAME))
DB_UPDATE_URL = 'https://sypexgeo.net/files/SxGeoCity_utf8.zip'
