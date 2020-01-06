from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR

ADMIN_NAMESPACE = 'admin'


def get_add_url(app_label, model_name, popup=False):
    """ Возвращает ссылку на добавление сущности в админке """
    try:
        url = reverse(
            '{}:{}_{}_add'.format(ADMIN_NAMESPACE, app_label, model_name)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?%s=id&%s=1' % (TO_FIELD_VAR, IS_POPUP_VAR)
        return url


def get_change_url(app_label, model_name, pk, popup=False):
    """ Возвращает ссылку на редактирование сущности в админке """
    try:
        url = reverse(
            '{}:{}_{}_change'.format(ADMIN_NAMESPACE, app_label, model_name),
            args=(pk,)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?%s=id&%s=1' % (TO_FIELD_VAR, IS_POPUP_VAR)
        return url


def get_delete_url(app_label, model_name, pk, popup=False):
    """ Возвращает ссылку на удаление сущности в админке """
    try:
        url = reverse(
            '{}:{}_{}_delete'.format(ADMIN_NAMESPACE, app_label, model_name),
            args=(pk,)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?%s=id&%s=1' % (TO_FIELD_VAR, IS_POPUP_VAR)
        return url


def add_related_attrs(instance_or_model, popup=False):
    """
        Возвращает URL, "onclick" и "id" для формирования ссылки на добавление сущности
        через Popup-окно.

        Пример:
            link_attrs = admin_utils.add_related_attrs(obj)
            return '<a href="{href}" id="{id}" onclick="{onclick}">{text}</a>'.format(
                text = str(obj),
                **link_attrs
            )
    """
    meta = getattr(instance_or_model, '_meta')
    return {
        'href': get_add_url(meta.app_label, meta.model_name, popup=popup),
        'onclick': 'showAddAnotherPopup(this); return false;',
        'id': 'add_id_%s' % meta.model_name,
    }


def change_related_attrs(instance, popup=False):
    """
        Возвращает URL, "onclick" и "id" для формирования ссылки на изменение сущности
        через Popup-окно.

        Пример:
            link_attrs = admin_utils.change_related_attrs(obj)
            return '<a href="{href}" id="{id}" onclick="{onclick}">{text}</a>'.format(
                text = str(obj),
                **link_attrs
            )
    """
    meta = getattr(instance, '_meta')
    return {
        'href': get_change_url(meta.app_label, meta.model_name, instance.pk, popup=popup),
        'onclick': 'showRelatedObjectPopup(this); return false;',
        'id': 'change_id_%s' % meta.model_name,
    }


def delete_related_attrs(instance, popup=False):
    """
        Возвращает URL, "onclick" и "id" для формирования ссылки на удаление сущности
        через Popup-окно.

        Пример:
            link_attrs = admin_utils.delete_related_attrs(obj)
            return '<a href="{href}" id="{id}" onclick="{onclick}">{text}</a>'.format(
                text = str(obj),
                **link_attrs
            )
    """
    meta = getattr(instance, '_meta')
    return {
        'href': get_delete_url(meta.app_label, meta.model_name, instance.pk, popup=popup),
        'onclick': 'showRelatedObjectPopup(this); return false;',
        'id': 'change_id_%s' % meta.model_name,
    }
