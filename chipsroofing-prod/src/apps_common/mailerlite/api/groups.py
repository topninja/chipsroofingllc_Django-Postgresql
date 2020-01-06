from .base import request, parse_filters


def get_all(limit=100, offset=0, filters=None):
    """ Получение всех списков подписчиков """
    return request('groups', params={
        'limit': limit,
        'offset': offset,
        'filters': parse_filters(filters),
    })


def get(group_id):
    """ Получение информации о списке подписчиков """
    return request('groups/%d' % group_id)


def create(name):
    """ Создание списка подписчиков """
    return request('groups', method='POST', data={
        'name': name,
    })


def update(group_id, name):
    """ Обновление списка подписчиков """
    return request('groups/%d' % group_id, method='PUT', data={
        'name': name,
    })


def delete(group_id):
    """ Удаление списка """
    return request('groups/%d' % group_id, method='DELETE')
