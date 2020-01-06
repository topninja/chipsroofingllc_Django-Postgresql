"""
    Плагин соцкнопок.
    Включает соцкнопки "Поделиться", автопостинг в соцсети, виджет Instagram и блок ссылок на соцсети.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_networks',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'social_networks',
                    'icon': 'icon-bullhorn',
                    'models': (
                        'FeedPost',
                        'SocialLinks',
                        'SocialConfig',
                    ),
                },
                ...
            }

        urls.py:
            ...
            url(r'^dladmin/social/', include('social_networks.admin_urls', namespace='admin_social_networks')),
            url(r'^social/', include('social_networks.urls', namespace='social_networks')),
            ...


    Соцкнопки "Поделиться":
        # Нужно подключить JS и SCSS

        template.html:
            {% load share_buttons %}

            <div class="social-buttons no-counter">
              {% share_button 'vk' %}
              {% share_button 'fb' %}
              {% share_button 'tw' %}
              {% share_button 'gp' %}
              {% share_button 'li' %}
              {% share_button 'pn' %}
            </div>

    Ссылки на соцсети:
        # Нужно подключить SCSS

        template.html:
            {% load social_links %}

            <!-- Вывод ссылок -->
            {% social_links %}

            <!-- Вывод ссылок с дополнительным классом -->
            {% social_links classes='custom-css-classes' %}

    Виджет Instagram:
        # Нужно подключить JS и SCSS

        template.html:
            {% load instagram %}

            <!-- Вывод постов юзера -->
            {% instagram_widget user_id=1485581141 limit=6 %}

            <!-- Вывод постов по хэштегу -->
            {% instagram_widget tag="Moscow" limit=6 %}

    Автопостинг:
        Для Google Plus необходимо зарегистрироваться в https://hootsuite.com
        Для остальных соцсетей нужно настроить cron на выполнение
            python3 manage.py autopost

        # crontab
            */15 * * * * . $HOME/.profile; ~/project.com/env/bin/python3 ~/project.com/src/manage.py autopost

        admin.py:
            from social_networks.admin import AutoPostMixin
            ...

            class PostAdmin(SeoModelAdminMixin, AutoPostMixin, admin.ModelAdmin):
                ...
                def get_autopost_text(self, obj):
                    return obj.note

"""

default_app_config = 'social_networks.apps.Config'
