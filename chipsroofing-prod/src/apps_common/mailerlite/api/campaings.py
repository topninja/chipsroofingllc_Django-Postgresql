from .base import request

STATUS_DRAFT = 'draft'
STATUS_OUTBOX = 'outbox'
STATUS_SENT = 'sent'
STATUSES = [STATUS_DRAFT, STATUS_OUTBOX, STATUS_SENT]

ACTION_SEND = 'send'
ACTION_CANCEL = 'cancel'
ACTIONS = [ACTION_SEND, ACTION_CANCEL]


def get_all(status=STATUS_SENT, limit=100, offset=0):
    """ Получение всех рассылок со статусом status """
    if status not in STATUSES:
        raise ValueError('invalid campaign status: %s' % status)

    return request('campaigns/%s' % status, params={
        'limit': limit,
        'offset': offset,
    })


def create(subject, groups, from_email, from_name, language='en'):
    """
        Создание рассылки.

        Метки:
            {$email} - user email
            {$name} - first name
            {$last_name} - last name
            {$company} - user company
    """
    return request('campaigns', method='POST', data={
        'type': 'regular',
        'subject': subject,
        'from': from_email,
        'from_name': from_name,
        'groups': groups,
        'language': language,
    })


def content(campaign_id, html, plain):
    """
        Установка содержимого рассылки.
        ОБЯЗАТЕЛЬНО наличие ссылки на отписку:
            <a href="{$unsubscribe}">Unsubscribe</a>

        Метки:
            {$url} - URL to your HTML newsletter
            {$email} - user email
            {$name} - first name
            {$last_name} - last name
            {$company} - user company
            {$unsubscribe} - unsubscribe link
    """
    return request('campaigns/%d/content' % campaign_id, method='PUT', data={
        'html': html,
        'plain': plain,
        'auto_inline': 'true',
    })


def action(campaign_id, action_type=ACTION_SEND):
    """
        Запуск/отмена рассылки.
        Параметр action: send/cancel
    """
    if action_type not in ACTIONS:
        raise ValueError('invalid action: %s' % action_type)

    return request('campaigns/%d/actions/%s' % (campaign_id, action_type), method='POST')
