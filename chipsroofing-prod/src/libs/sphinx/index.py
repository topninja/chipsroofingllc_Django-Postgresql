import logging
import numbers
from datetime import datetime
from collections import namedtuple, Iterable
from django.db import models
from django.utils.html import escape
from django.core.cache import caches
from django.core.exceptions import ValidationError
from . import conf

AttrType = namedtuple('AttrType', 'BOOL INT BIGINT FLOAT STRING TIMESTAMP MULTI JSON')
Attr = namedtuple('Attr', 'type default')
logger = logging.getLogger('sphinx')
cache = caches[conf.CACHE_BACKEND]


ATTR_TYPE = AttrType(
    BOOL='bool',
    INT='int',
    BIGINT='bigint',
    FLOAT='float',
    STRING='string',
    TIMESTAMP='timestamp',
    MULTI='multi',
    JSON='json',
)

# Словарь всех индексов. Заполняется в apps.py
ALL_INDEXES = {}


class SphinxScheme:
    def __init__(self, index_name):
        self.fields = {}
        self.attrs = {}
        self.index_name = index_name

    def __iter__(self):
        """ Генератор схемы индекса """
        yield """<sphinx:schema>"""

        # Fields
        for name, is_attribute in self.fields.items():
            if is_attribute:
                yield """<sphinx:field name="{}" attr="string"/>""".format(name)
            else:
                yield """<sphinx:field name="{}"/>""".format(name)

        # Index Name
        yield """<sphinx:attr name="{}" type="string" default="{}"/>""".format(
            'index_name',
            self.index_name
        )

        # Attributes
        for name, attr in self.attrs.items():
            if attr.default is None:
                yield """<sphinx:attr name="{}" type="{}"/>""".format(name, attr.type)
            else:
                yield """<sphinx:attr name="{}" type="{}" default="{}"/>""".format(name, *attr)

        yield """</sphinx:schema>"""

    def add_fields(self, name, is_attribute=False):
        """ Добавление поля для полнотекстового поиска """
        if name in self.attrs:
            raise ValidationError("field '%s' already exists in 'attrs'" % name)

        self.fields[name] = is_attribute

    def add_attr(self, name, attr_type=ATTR_TYPE.STRING, default=None):
        """ Добавление аттрибута индекса """
        if name in self.fields:
            raise ValidationError("field '%s' already exists in 'fields'" % name)

        self.attrs[name] = Attr(attr_type, default)

    def format(self, document, *, doc_id):
        """ Форматирование документа по схеме """
        for name in self.fields:
            if name not in document:
                raise ValidationError("index '%s', document %d: field '%s' required" % (
                    self.index_name, doc_id, name
                ))
            else:
                document[name] = str(document[name])

        for name, attr in self.attrs.items():
            if name in document:
                value = document[name]
                if attr.type == ATTR_TYPE.TIMESTAMP:
                    # Timestamp
                    if isinstance(value, datetime):
                        document[name] = int(value.timestamp())
                    elif not isinstance(value, numbers.Integral):
                        try:
                            int(value)
                        except (TypeError, ValueError):
                            raise ValidationError("index '%s', document %d: field '%s' should be a datetime or int" % (
                                self.index_name, doc_id, name
                            ))
                elif attr.type == ATTR_TYPE.MULTI:
                    # Multivalue
                    if isinstance(value, Iterable):
                        document[name] = ','.join(map(str, value))
                    else:
                        raise ValidationError("index '%s', document %d: field '%s' should be an iterable" % (
                            self.index_name, doc_id, name
                        ))
                if attr.type == ATTR_TYPE.BOOL:
                    try:
                        document[name] = int(bool(value))
                    except (TypeError, ValueError):
                        raise ValidationError("index '%s', document %d: field '%s' should be a bool" % (
                            self.index_name, doc_id, name
                        ))
            elif attr.default is None:
                raise ValidationError("index '%s', document %d: field '%s' required" % (
                    self.index_name, doc_id, name
                ))
        allowed_names = tuple(self.fields) + tuple(self.attrs)
        for name in document:
            if name not in allowed_names:
                raise ValidationError("index '%s', document %d: unknown field '%s'" % (
                    self.index_name, doc_id, name
                ))

        return document


class SphinxXMLIndex:
    name = ''
    model = None
    scheme_class = None

    def __init__(self):
        if not self.model or not issubclass(self.model, models.Model):
            raise AttributeError("'model' should be a subclass of models.Model")

        if not self.scheme_class or not issubclass(self.scheme_class, SphinxScheme):
            raise AttributeError("'scheme' should be a subclass of sphinx.SphinxScheme")

        self.scheme = self.scheme_class(self.name)

    def __iter__(self):
        """ Генератор XML """
        yield """<?xml version="1.0" encoding="utf-8"?><sphinx:docset xmlns:sphinx="http://sphinxsearch.com/">"""
        yield from self.scheme

        for instance in self.get_queryset():
            docuemnt = self.build_document(instance)
            try:
                document = self.scheme.format(docuemnt, doc_id=instance.id)
            except ValidationError as e:
                logger.error(e.message)
                return
            else:
                output = """<sphinx:document id="{0}">""".format(instance.id)
                for key, value in document.items():
                    output += """<{0}>{1}</{0}>""".format(
                        key, escape(value) or ''
                    )
                output += """</sphinx:document>"""
                yield output

        yield """</sphinx:docset>"""

    def get_queryset(self):
        """ QuerySet всех индексируемых документов """
        return self.model.objects.all()

    def build_document(self, instance):
        """ Должен вернуть словарь данных документа, в соответствии со схемой """
        raise NotImplementedError

    def _build_breakpoint_name(self, name):
        return 'sphinx_%s' % (name or self.name)

    def set_breakpoint(self, value, name=None):
        """ Для дельта-индексов: сохранение точки в кэш """
        bp_name = self._build_breakpoint_name(name)
        cache.set(bp_name, value, timeout=7*24*3600)

    def get_breakpoint(self, name=None):
        """ Для дельта-индексов: загрузка точки в кэш """
        bp_name = self._build_breakpoint_name(name)
        return cache.get(bp_name)
