"""
    Поле для выбора иконки из спрайта.

    Установка:
        settings.py:
            INSTALLED_APS = (
                ...
                'libs.sprite_image',
                ...
            )

    Пример:
        # models.py:
            class MyModel(models.Model):
                ICONS = (
                    ('no_defence', (-230, 0)),
                    ('area', (-260, 0)),
                    ('touch', (-290, 0)),
                    ('leaf', (-320, 0)),
                    ('shield', (-350, 0)),
                    ('dots', (-380, 0)),
                    ('no_bacterial', (-410, 0)),
                )

                ...

                icon = SpriteImageField(_('icon'),
                    sprite='img/sprite.svg',
                    size=(30, 30),
                    choices=ICONS,
                    default=ICONS[0][0],
                    background='#FFFFFF',
                )

        # template.html:
            # Вывод имени ключа
            <div class="{{ object.icon }}">

            # Вывод координат
            <div style="background-position: {{ object.icon.x }}px {{ object.icon.y }}px">

            # Вывод ссылки на картинку
            <div style="background-image: {{ object.icon.url }}">

"""
