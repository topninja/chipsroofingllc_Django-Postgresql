import re
import logging
from xml.dom import minidom
from urllib import request, error
from django.utils.html import strip_tags
from social_networks.api import youtube

PROVIDERS = {}

logger = logging.getLogger(__name__)


class ProviderMetaclass(type):
    """ Автоматическая регистрация класса провайдера """
    def __init__(cls, what, bases=None, attrs=None):
        super().__init__(what, bases, attrs)
        if cls.name:
            PROVIDERS[cls.name] = cls


class BaseProvider(metaclass=ProviderMetaclass):
    name = ''
    url_pattern = ''
    parse_patterns = ()

    @classmethod
    def find_key(cls, url):
        for pattern in cls.parse_patterns:
            match = pattern.match(url)
            if match:
                return match.group(1)
        raise ValueError('Bad video URL: %s' % url)

    @classmethod
    def parse(cls, url):
        """ Парсинг URL """
        return cls.name, cls.find_key(url)

    @classmethod
    def build_url(cls, video_key):
        """ Конструирование ссылки на видео по ключу """
        return cls.url_pattern.format(video_key)

    @classmethod
    def get_info(cls, video_key):
        return None


class YoutubeProvider(BaseProvider):
    name = 'youtube'
    url_pattern = 'https://www.youtube.com/watch?v={}'
    parse_patterns = (
        re.compile(r'(?:https?:)?//(?:www\.)?youtube\.com/watch\?v=([-\w]{11,})'),
        re.compile(r'(?:https?:)?//(?:www\.)?youtube\.com/(?:v|embed)/([-\w]{11,})'),
        re.compile(r'(?:https?:)?//youtu\.be/([-\w]{11,})'),
    )

    @classmethod
    def get_info(cls, video_key):
        data = youtube.get_video_info(video_key)
        if not data:
            return {}

        thumbnails = data['thumbnails']
        if 'maxres' in thumbnails:
            data['preview_url'] = thumbnails['maxres']['url']
        elif 'standard' in thumbnails:
            data['preview_url'] = thumbnails['standard']['url']
        elif 'high' in thumbnails:
            data['preview_url'] = thumbnails['high']['url']
        else:
            data['preview_url'] = thumbnails['medium']['url']

        return data


class VimeoProvider(BaseProvider):
    name = 'vimeo'
    url_pattern = 'https://vimeo.com/{}'
    parse_patterns = (
        re.compile(r'(?:https?:)?//(?:www\.)?vimeo\.com/groups/[^/]+/videos/(\d+)'),
        re.compile(r'(?:https?:)?//(?:www\.)?vimeo\.com/(?:channels|ondemand)/[^/]+/(\d+)'),
        re.compile(r'(?:https?:)?//(?:www\.)?vimeo\.com/(\d+)'),
    )

    @classmethod
    def get_info(cls, video_key):
        req = request.Request('http://vimeo.com/api/v2/video/%s.xml' % video_key, method='GET')
        try:
            logger.debug('{0.method} {0.full_url}'.format(req))
            response = request.urlopen(req, timeout=3)
        except error.URLError:
            return None

        if response.status != 200:
            return None

        dom = minidom.parseString(response.read())
        title = dom.getElementsByTagName('title').item(0)
        description = dom.getElementsByTagName('description').item(0)
        description = description.firstChild.data
        description = re.sub(r'<br\s*/?>\s*', '\n', description)
        thumbnail_large = dom.getElementsByTagName('thumbnail_large').item(0)
        width = dom.getElementsByTagName('width').item(0)
        width = int(width.firstChild.data)
        height = dom.getElementsByTagName('height').item(0)
        height = int(height.firstChild.data)
        embed_width = min(640, width)
        embed_height = int(embed_width * height / width)
        code = '<iframe src="//player.vimeo.com/video/{}" ' \
               'width="{}" height="{}" frameborder="0" ' \
               'webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
        return {
            'title': title.firstChild.data,
            'description': strip_tags(description),
            'preview_url': thumbnail_large.firstChild.data.replace('webp', 'jpg'),
            'embed': code.format(video_key, embed_width, embed_height)
        }


class RutubeProvider(BaseProvider):
    name = 'rutube'
    url_pattern = 'https://rutube.ru/video/{}'
    parse_patterns = (
        re.compile(r'(?:https?:)?//(?:www\.)?rutube\.ru/video/(\w{32})'),
    )

    @classmethod
    def get_info(cls, video_key):
        req = request.Request('http://rutube.ru/api/video/%s/?format=xml' % video_key, method='GET')
        try:
            logger.debug('{0.method} {0.full_url}'.format(req))
            response = request.urlopen(req, timeout=3)
        except error.URLError:
            return None

        if response.status != 200:
            return None

        dom = minidom.parseString(response.read())

        title = dom.getElementsByTagName('title').item(0)
        description = dom.getElementsByTagName('description').item(0)
        thumbnail = dom.getElementsByTagName('thumbnail_url').item(0)
        embed = dom.getElementsByTagName('html').item(0)

        return {
            'title': title.firstChild.data,
            'description': description.firstChild.data,
            'preview_url': thumbnail.firstChild.data,
            'embed': embed.firstChild.data
        }
