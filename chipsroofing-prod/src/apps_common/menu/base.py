from django.forms.utils import flatatt
from django.shortcuts import resolve_url
from django.core.urlresolvers import NoReverseMatch
from django.utils.functional import cached_property


class BaseMenuObject:
    __slots__ = ('_is_active', '_childs',)

    def __init__(self):
        self._is_active = False
        self._childs = []

    def __iter__(self):
        return iter(self._childs)

    def __getitem__(self, index):
        return self._childs[index]

    @property
    def is_active(self):
        return self._is_active

    @property
    def childs(self):
        return self._childs

    def append(self, *items):
        for item in items:
            item._parent = self
        self._childs.extend(items)
        return self

    def insert(self, index, item):
        item._parent = self
        self._childs.insert(index, item)
        return self

    def activate(self):
        self._is_active = True


class Menu(BaseMenuObject):
    """ Класс меню """
    def _recursive_search(self, root, key=lambda item: True):
        result = []

        for item in root.childs:
            if item.childs:
                result.extend(self._recursive_search(item, key))

            if key(item):
                result.append(item)

        return result

    @cached_property
    def items(self):
        return self._recursive_search(self)


class MenuItem(BaseMenuObject):
    """ Пункт меню """
    __slots__ = Menu.__slots__ + (
        '_parent', '_item_id',
        '_title', '_url', '_classes', '_attrs',
    )

    def __init__(self, title, url, attrs=None, item_id=''):
        super().__init__()
        self._parent = None
        self._item_id = item_id
        self._title = str(title)

        try:
            self._url = resolve_url(url)
        except NoReverseMatch:
            self._url = url

        if attrs is None:
            self._classes = ''
            self._attrs = ''
        else:
            self._classes = attrs.pop('class', '')
            self._attrs = flatatt(attrs)

    def __repr__(self):
        return '{classname}({item.title!r}, {item.url!r}, {item.attrs!r}, {item._item_id!r})'.format(
            classname=self.__class__.__name__,
            item=self
        )

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def classes(self):
        return self._classes

    @property
    def attrs(self):
        return self._attrs

    @property
    def item_id(self):
        return self._item_id

    def activate(self):
        super().activate()
        try:
            self._parent.activate()
        except AttributeError:
            pass
