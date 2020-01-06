"""
    Хранилища файлов.

    1) Разделение статики по доменам:
        # settings.py
            MEDIA_URLS = (
                '//media1.local.com',
                '//media2.local.com',
            )

            TEMPLATES = {
                'context_processors': (
                    ...
                    'libs.storages.context_processors.media_urls',
                    ...
                )
            }

        # template.html
            {% for domain in MEDIA_URLS %}
                <link rel="dns-prefetch" href="{{ domain }}">
                <link rel="preconnect" href="{{ domain }}">
            {% endfor %}
"""
