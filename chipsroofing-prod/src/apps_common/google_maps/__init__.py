"""
    Зависит от:
        social_networks
        libs.coords

    Необходимо подключить:
        google_maps/js/core.js

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'google_maps',
                ...
            )

            TEMPLATES = [
                {
                    ...
                    'OPTIONS': {
                        'context_processors': (
                            ...
                            'social_networks.context_processors.google_apikey',
                        ),
                    }
                },
            ]

    Настройки (settings.py):
        GOOGLE_MAP_ADMIN_WIDTH - ширина карты в админке (по умолчанию 100%)
        GOOGLE_MAP_ADMIN_HEIGHT - высота карты в админке (по умолчанию 300px)
        GOOGLE_MAP_ADMIN_ZOOM - зум карты в админке (по умолчанию 16)

        GOOGLE_MAP_STATIC_WIDTH - ширина статических карт (по умолчанию 300px)
        GOOGLE_MAP_STATIC_HEIGHT - высота статических карт (по умолчанию 200px)
        GOOGLE_MAP_STATIC_ZOOM - зум статических карт (по умолчанию 14)

    Примеры:
        script.py:
            from google_maps.api import geocode
            from google_maps.models import geocode_cached

            # Получить координаты по адресу.
            lng, lat = geocode('Тольятти, Мира 35', timeout=0.5)

            # Получить координаты по адресу с кэшированием результатов
            lng, lat = geocode_cached('Тольятти, Мира 35', timeout=0.5)

        models.py:
            from google_maps.fields import GoogleCoordsField
            ...

            address = models.CharField(_('address'), max_length=255, blank=True)
            coords = GoogleCoordsField(_('coordinates'), null=True, blank=True)

        page.js:
            $(document).ready(function() {
                var gmap = GMap('#gmap', {
                    zoom:13
                }).on('ready', function() {
                    var marker = GMapMarker({
                        map: this,
                        position: GMapPoint(53.510171, 49.418785),
                        hint: 'First',
                        balloon: '<p>Hello</p>'
                    })
                });
            });

        Admin Javascript:
            // Получение координат по адресу в другом поле
            $(document).on('change', '#id_address', function() {
                var gmap = $('#id_coords').next('.google-map').data('gmap');
                gmap.geocode($(this).val(), function(point) {
                    var marker = this.markers[0];
                    if (marker) {
                        marker.position(point);
                    } else {
                        marker = GMapMarker({
                            map: this,
                            position: point
                        })
                    }

                    marker.trigger('dragend');
                    this.panTo(point);
                });
            });

        template.html:
            {% load google_maps %}

            <!-- Статичная карта с зумом 15 размера 300x200 -->
            <img src='{{ address|google_map_static:"15,300,200" }}'>

            <!-- Ссылка на карту в сервисе Google -->
            <a href='{{ address|google_map_external:15 }}' target='_blank'>посмотреть карту</a>
"""

default_app_config = 'google_maps.apps.Config'
