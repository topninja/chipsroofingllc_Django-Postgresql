(function($) {
    'use strict';

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Для отлова события загрузки всех блоков можно
        использовать событие "loaded.placeholder":
            $(document).on('loaded.placeholder', function() {

            })
     */

    /** @namespace window.js_storage.placeholder_url */

    var fetchPlaceholderParts = function(name, parts) {
        var query_data = [];
        for (var i = 0, l = parts.length; i < l; i++) {
            query_data.push(parts[i].params);
        }

        $.ajax({
            url: window.js_storage.placeholder_url + name + '/',
            type: 'POST',
            data: {
                name: name,
                arr: query_data
            },
            dataType: 'json',
            success: function(response) {
                if (response.parts) {
                    if (parts.length !== response.parts.length) {
                        console.warn('Length error! Queried: ' + parts.length + '; rendered ' + response.parts.length);
                    }

                    for (i = 0, l = Math.min(parts.length, response.parts.length); i < l; i++) {
                        var $placeholder = $(parts[i].element);
                        $placeholder.replaceWith(response.parts[i]);
                    }
                }

                // callback event
                $(document).trigger('loaded.placeholder', name);
            }
        });
    };


    $(document).ready(function() {
        var placeholders = {};

        $('.placeholder').each(function() {
            var $placeholder = $(this);
            var data = $placeholder.data();

            var name = data.name;
            if (!name) {
                console.warn('not found name in placeholder');
                $placeholder.remove();
                return;
            }

            var params = {
                _: 1    // чтобы не терялся индекс в AJAX из-за пустого объекта
            };
            for (var key in data) {
                if (data.hasOwnProperty(key) && (key !== 'name')) {
                    params[key] = data[key];
                }
            }

            var placeholder = {
                element: this,
                name: name,
                params: params
            };

            if (name in placeholders) {
                placeholders[name].push(placeholder);
            } else {
                placeholders[name] = [placeholder];
            }
        });


        for (var name in placeholders) {
            if (placeholders.hasOwnProperty(name)) {
                fetchPlaceholderParts(name, placeholders[name]);
            }
        }
    });

})(jQuery);
