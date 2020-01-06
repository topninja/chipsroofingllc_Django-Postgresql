from .base import request

STATUS_ACTIVE = 'active'
STATUS_BOUNCED = 'bounced'
STATUS_UNSUBSCRIBED = 'unsubscribed'
STATUS_JUNK = 'junk'
STATUS_UNCONFIRMED = 'unconfirmed'
STATUSES = [STATUS_ACTIVE, STATUS_BOUNCED, STATUS_UNSUBSCRIBED, STATUS_JUNK, STATUS_UNCONFIRMED]


def _build_fields(**fields):
    """
        Формирование дополнительных данных подписчика
    """
    result = {}
    for key, value in fields.items():
        value = value.strip()
        if not value:
            continue
        result[key.lower()] = value
    return result


def get_all(group_id, status=None, limit=100, offset=0, filters=None):
    """
        Получение подписчиков из списка
    """
    if status is None:
        return request('groups/%d/subscribers' % (group_id,), params={
            'limit': limit,
            'offset': offset,
            'filters': filters,
        })
    else:
        if status not in STATUSES:
            raise ValueError('invalid subscriber status: %s' % status)

        return request('groups/%d/subscribers/%s' % (group_id, status), params={
            'limit': limit,
            'offset': offset,
            'filters': filters,
        })


def get(id_or_email):
    """ Получение информации о подписчике """
    return request('subscribers/%s' % id_or_email)


def get_groups(id_or_email):
    """ Получение групп, в которых состоит подписчик """
    return request('subscribers/%s/groups' % id_or_email)


def create(email, status=None, resubscribe=False, **fields):
    """
        Создание подписчика без привязки к группе
    """
    data = {
        'email': email,
        'resubscribe': '1' if resubscribe else '0',
    }

    if status:
        if status not in [STATUS_ACTIVE, STATUS_UNCONFIRMED]:
            raise ValueError('invalid subscriber status: %s' % status)
        else:
            data['type'] = status

    fields = _build_fields(**fields)
    if fields:
        data['fields'] = fields

    return request('subscribers', method='POST', data=data)


def subscribe(email, group_id, status=None, resubscribe=False, **fields):
    """
        Привязка подписчика к группе
    """
    data = {
        'email': email,
        'resubscribe': '1' if resubscribe else '0',
    }

    if status:
        if status not in [STATUS_ACTIVE, STATUS_UNCONFIRMED]:
            raise ValueError('invalid subscriber status: %s' % status)
        else:
            data['type'] = status

    fields = _build_fields(**fields)
    if fields:
        data['fields'] = fields

    return request('groups/%d/subscribers' % group_id, method='POST', data=data)


def bulk_subscribe(group_id, subscribers, resubscribe=False):
    """
        Массовая подписка на группу
    """
    return request('groups/%d/subscribers/import' % group_id, method='POST', data={
        'subscribers': subscribers,
        'resubscribe': '1' if resubscribe else '0',
    })


def update(id_or_email, status=None, **fields):
    """
        Обновление данных пользователя
    """
    data = {}
    if status:
        if status not in [STATUS_ACTIVE, STATUS_UNSUBSCRIBED]:
            raise ValueError('invalid subscriber status: %s' % status)
        else:
            data['type'] = status

    fields = _build_fields(**fields)
    if fields:
        data['fields'] = fields

    return request('subscribers/%s' % id_or_email, method='PUT', data=data)


def delete(id_or_email, group_id):
    """
        Удаление подписчика из списка
    """
    return request('groups/%d/subscribers/%s' % (group_id, id_or_email), method='DELETE')


def search(query='', limit=100, offset=0, minimized=True):
    """ Поиск по подписчикам """
    return request('subscribers/search', params={
        'query': query,
        'limit': limit,
        'offset': offset,
        'minimized': 'true' if minimized else 'false',
    })


