import inspect
from collections import deque
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from .models import SeoConfig, SeoData
from .opengraph import Opengraph, TwitterCard

TITLE_JOIN_WITH = str(getattr(settings, 'SEO_TITLE_JOIN_WITH', ' | '))


class TitleDescriptor:
    """
        Дескриптор аттрибута, который инкапсулирует дэк частей <title>.
        Присваивание значения этому аттрибуту добавляет это значение в дэк.
    """
    def __init__(self, deque_name):
        self.deque_name = deque_name

    def __get__(self, instance, owner):
        """ Возврат полного заголовка в виде строки """
        title_deque = instance.__dict__.get(self.deque_name, None)
        if title_deque is None:
            instance.__dict__[self.deque_name] = title_deque = deque()

        return title_deque

    def __set__(self, instance, value):
        title_deque = instance.__dict__.get(self.deque_name, None)
        if title_deque is None:
            instance.__dict__[self.deque_name] = title_deque = deque()

        title_deque.appendleft(value)


class SeoMetaClass(type):
    """
        Запоминаем все не вызываемые члены класса, чтобы
        по ним фильтровать сео-данные.
    """
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        members = inspect.getmembers(cls, lambda x: not callable(x))
        cls._fields = tuple(name for name, field in members if not name.startswith('_'))
        return cls


class Seo(metaclass=SeoMetaClass):
    title = TitleDescriptor('_title_deque')
    keywords = ''
    description = ''

    # мета-информация
    canonical = ''
    next = ''
    prev = ''
    noindex = False

    # Share-информация
    og_title = ''
    og_image = ''
    og_description = ''

    def __init__(self):
        site_seoconfig = SeoConfig.get_solo()
        self.set({
            'title': site_seoconfig.title,
            'keywords': site_seoconfig.keywords,
            'description': site_seoconfig.description,
        })

    @staticmethod
    def get_for(instance):
        """ Получение SeoData для объекта """
        ct = ContentType.objects.get_for_model(type(instance))
        try:
            return SeoData.objects.get(
                content_type=ct,
                object_id=instance.pk
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return None

    @staticmethod
    def get_or_create_for(instance):
        """ Получение или создание SeoData для объекта """
        ct = ContentType.objects.get_for_model(type(instance))
        try:
            return SeoData.objects.get(
                content_type=ct,
                object_id=instance.pk
            )
        except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
            return SeoData(
                content_type=ct,
                object_id=instance.pk
            )

    def set(self, dictionary):
        """
            Присваивание данных словаря в аттрибуты текущего объекта.
        """
        if not isinstance(dictionary, dict):
            raise TypeError("'Seo.apply_dict()' requires a dict instance. %s ")

        for key, value in dictionary.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def set_data(self, instance, defaults=None):
        """
            Получение SeoData из объекта instance и установка данных из него.
        """
        defaults = defaults or {}

        # если у объекта объявлен get_absolute_url - ставим его как canonical по умолчанию
        if hasattr(instance, 'get_absolute_url') and not self.canonical and 'canonical' not in defaults:
            defaults['canonical'] = getattr(instance, 'get_absolute_url')()

        seodata = self.get_for(instance)
        if seodata is None:
            self.set(defaults)
            return

        # конвертация SeoData в словарь, совместимый с Seo-объектом
        seodata_formatted = {
            'title': seodata.title,
            'keywords': seodata.keywords,
            'description': seodata.description,

            'canonical': seodata.canonical,
            'noindex': seodata.noindex,

            'og_title': seodata.og_title,
            'og_image': seodata.og_image,
            'og_description': seodata.og_description,
        }

        data = {
            key: seodata_formatted.get(key) or defaults.get(key) or None
            for key in self._fields
        }

        # присваивание первого не ложного значения к соответствующему аттрибуту
        self.set(data)

    def set_title(self, instance, default=None):
        """
            Алиас для упрощения добавления заголовков из родительских категорий.

            Пример:
                seo = Seo()
                seo.set_title(shop, default=shop.title)
        """
        seodata = self.get_for(instance)
        title = (seodata and seodata.title) or default
        if title:
            self.title = title

    def save(self, request):
        """
            Рендеринг Seo-данных в итоговый словарь
        """
        result = {}

        # Title
        title_parts = list(filter(bool, map(str, self.title)))
        if TITLE_JOIN_WITH:
            result['title'] = mark_safe(TITLE_JOIN_WITH.join(title_parts))
        else:
            result['title'] = mark_safe(title_parts[0]) if title_parts else ''

        # keywords, description
        for attrname in ('keywords', 'description'):
            value = getattr(self, attrname)
            if value:
                result[attrname] = str(value)

        # canonical
        if self.canonical:
            result['canonical'] = request.build_absolute_uri(self.canonical)

        # next
        if self.next:
            result['next'] = request.build_absolute_uri(self.next)

        # prev
        if self.prev:
            result['prev'] = request.build_absolute_uri(self.prev)

        # noindex
        if self.noindex:
            result['noindex'] = True

        # Share-данные
        share_data = {
            'url': request.build_absolute_uri(self.canonical or request.path_info),
            'image': self.og_image,
            'title': self.og_title or title_parts[0] if title_parts else '',
            'description': self.og_description or self.description,
        }

        opengraph = Opengraph(request)
        opengraph.update(share_data)
        result['opengraph'] = opengraph

        twitter_card = TwitterCard(request)
        twitter_card.update(share_data)
        result['twitter_card'] = twitter_card

        request.seo = result
