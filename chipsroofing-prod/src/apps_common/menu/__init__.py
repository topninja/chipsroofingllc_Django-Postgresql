"""
    Меню сайта.

    Установка:
        INSTALLED_APPS = (
            ...
            'menu',
            ...
        )

        MIDDLEWARE_CLASSES = (
            ...
            'menu.middleware.MenuMiddleware',
            ...
        )

    Пример:
        # menu/menus.py
            def main():
                menu = Menu()
                menu.append(
                    MenuItem('News', '/news/').append(
                        MenuItem('Post 1', '/news/post-1/'),
                        MenuItem('Post 2', '/news/post-2/'),
                    ),
                    MenuItem('Articles', '/articles/', item_id='articles'),
                )
                return menu

        # template.html
            ...
            {% menu 'main' %}
            ...

        # views.py:
            from menu import activate_menu
            ...
            # Ручная установка активного пункта меню по его item_id
            activate_menu(request, 'articles')
"""

default_app_config = 'menu.apps.Config'
