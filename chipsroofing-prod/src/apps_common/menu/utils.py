import inspect
from . import menus


def get_menus(request):
    """ Получение всех меню, объявленных в файле menus.py """
    result = {}
    for name, func in inspect.getmembers(menus, inspect.isfunction):
        if func.__module__ == 'menu.menus':
            result[name] = func(request)

    return result


def activate_menu(request, item_id):
    """
        Активация пункта во всех меню по его item_id.
    """
    all_menus = getattr(request, '_menus', None)
    if not all_menus:
        return

    for menu in all_menus.values():
        activate_by_id(menu, item_id)


def activate_by_url(menu, url):
    """
        Активация пункта меню по урлу
    """
    if menu.is_active:
        return

    # пункты меню, которые соответсвуют урлу (префиксно)
    matches = [item for item in menu.items if url.startswith(item.url)]
    if not matches:
        return
    elif len(matches) == 1:
        matches[0].activate()
    else:
        # ищем самый длинный из совпавших урлов
        sorted_matches = sorted(matches, key=lambda item: len(item.url.split('/')), reverse=True)
        sorted_matches[0].activate()


def activate_by_id(menu, item_id):
    """
        Активация пункта меню по ID
    """
    if menu.is_active:
        return

    for item in menu.items:
        if item.item_id == item_id:
            item.activate()
            return
