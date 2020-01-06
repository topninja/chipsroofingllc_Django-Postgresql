(function($) {

    var init_map_field = function() {
        var $field = $(this);
        if ($field.closest('.empty-form').length) {
            return
        }

        // Создание контейнера для карты
        var field_data = $field.data();
        var $map = $('<div>').addClass('google-map');
        if (field_data.width) {
            $map.width(field_data.width)
        }
        $map.height(field_data.height || '300px');
        $map.css('margin-top', '10px');
        $field.after($map);

        // карта
        GMap($map, {
            zoom: parseInt(field_data.zoom) || 16
        }).on('ready', function() {
            var coords_str = $field.val();
            if (coords_str) {
                var point = GMapPoint.fromString(coords_str);
            } else {
                point = GMapPoint(40.70583, -74.2588721);
            }

            var marker = GMapMarker({
                map: this,
                position: point,
                draggable: true
            }).on('dragend', function() {
                $field.val(this.position().toString());
            });

            this.center(point);

            // установка значения поля при двойном клике
            this.on('dblclick', function(event) {
                /** @namespace event.latLng */

                var point = GMapPoint.fromNative(event.latLng);
                marker.position(point);
                $field.val(point.toString());
            });
        }).on('resize', function() {
            var marker = this.markers[0];
            if (marker) {
                this.center(marker);
            }
        });
    };


    $(document).ready(function() {
        // Инициализация карт после добавления инлайна с картой
        if (window.Suit) {
            Suit.after_inline.register('google_map_inline', function(inline_prefix, row) {
                row.find('.google-map-field').each(init_map_field);
            })
        }
    }).on('google-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.google-map-field').each(init_map_field);
    }).on('change', '.google-map-field', function() {
        // Изменение карты при изменении координат в текстовом поле
        var $field = $(this);
        var coords_str = $field.val();
        if (!coords_str) {
            return
        }

        var gmap = $field.next('.google-map').data(GMap.prototype.DATA_KEY);
        if (!gmap) {
            console.error('GMap object not found');
            return;
        }

        var point = GMapPoint.fromString(coords_str);
        var marker = gmap.markers[0];
        if (marker) {
            marker.position(point);
        }
        gmap.panTo(point);
    }).on('click', '.nav-tabs li', function() {
        // TODO: костыль. Фикс карты, когда она в невидимой вкладке
        $('.google-map-field + .google-map').each(function() {
            var gmap = $(this).data(GMap.prototype.DATA_KEY);
            if (gmap) {
                google.maps.event.trigger(gmap.native, 'resize');
            }
        });
    });

})(jQuery);
