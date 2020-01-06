import logging
from .api import SphinxClient, SPH_SORT_EXTENDED
from .index import ALL_INDEXES
from . import conf

logger = logging.getLogger('sphinx')


class SearchError(Exception):
    @property
    def message(self):
        return self.args[0]


class SphinxSearchResult:
    __slots__ = ('_total', '_offset', '_matches')

    def __init__(self, total=0, offset=0, matches=()):
        self._total = total
        self._offset = offset
        self._matches = tuple(matches)

    def __iter__(self):
        return iter(self._matches)

    def __len__(self):
        """ Кол-во найденных элементов """
        return len(self._matches)

    def __repr__(self):
        return '%s(%s)' % (str(type(self).__name__), self._matches)

    @property
    def offset(self):
        """ Смещение найденных записей """
        return self._offset

    @property
    def total(self):
        """ Общее кол-во найденных записей """
        return self._total


class SphinxSearch:
    index = '*'
    limit = 50
    index_attr_name = 'index_name'

    # defaults
    filters = ()
    weights = None
    order_by = '@relevance DESC, @id DESC'

    def __init__(self):
        self.client = SphinxClient()
        self.client.SetServer(conf.HOST, conf.PORT)

    def fetch(self, query, filters=None, weights=None, order_by='', offset=0, limit=None, index=None):
        """ Выборка страницы результатов """
        self.client._error = ''
        self.client._warning = ''

        limit = limit or self.limit
        self.client.SetLimits(offset, limit)
        self.client.SetSortMode(SPH_SORT_EXTENDED, order_by or self.order_by)

        weights = weights or self.weights
        if weights:
            self.client.SetFieldWeights(weights)

        self.client.ResetFilters()
        filters = filters or self.filters
        for fieldname, values in filters:
            self.client.SetFilter(fieldname, values)

        index = index or self.index
        result = self.client.Query(query, index)
        if result is None:
            message = self.client._error or self.client._warning
            logger.error(message)
            raise SearchError(message)

        return SphinxSearchResult(result['total_found'], offset, result['matches'])

    def _to_dicts(self, result):
        """ Конвертация результата работы метода fetch() в словари """
        return SphinxSearchResult(result.total, result.offset, (
            {
                key: value.decode() if isinstance(value, bytes) else value
                for key, value in dict(record['attrs'], id=record['id']).items()
                }
            for record in result
        ))

    def fetch_dicts(self, query, **kwargs):
        """ Обертка над fetch, возвращающая словари """
        result = self.fetch(query, **kwargs)
        return self._to_dicts(result)

    def _to_models(self, result):
        """ Конвертация результата работы метода fetch() в экземпляры моделей """
        order_list = tuple(
            (record['id'], record['attrs'][self.index_attr_name].decode())
            for record in result
        )

        index_ids = {}
        for record in order_list:
            index_ids.setdefault(record[1], []).append(record[0])

        index_instances = {}
        for index_name, ids in index_ids.items():
            index = ALL_INDEXES[index_name]

            # Выборка из БД
            qs_method = getattr(self, '%s_queryset' % index_name, None)
            if qs_method is None:
                qs = index.model._default_manager.filter(pk__in=ids)
            else:
                qs = qs_method(index.model, ids)

            for instance in qs:
                index_instances[(instance.id, index_name)] = instance

        return SphinxSearchResult(result.total, result.offset, (
            index_instances[key_tuple]
            for key_tuple in order_list
            if key_tuple in index_instances
        ))

    def fetch_models(self, query, **kwargs):
        """ Обертка над fetch, возвращающая экземпляры моделей """
        result = self.fetch(query, **kwargs)
        return self._to_models(result)
