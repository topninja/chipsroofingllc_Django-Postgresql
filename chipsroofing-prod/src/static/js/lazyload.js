(function($) {

    /*
        Отложенная загрузка картинок.
        Необходимо добавить тэгу img класс "lazyload" и перенести атрибуты src/srcset/sizes в data.

        Зависит от:
            jquery.inspectors.js

        Дополнительные классы:
            onview      - загрузка, когда элемент станет видимым

        Принудительно начать загрузку:
            $('.lazyload').loadImage();

        Пример:
            <img data-src="read-image.jpg" class="lazyload onview">

        Примеры с плейсхолдером:
            // simple
            <div data-src="read-image.jpg" class="lazyload onview"></div>

            // extended
            <div class="lazyload" style="width: {{ image.width }}px" data-src="{{ image.url }}">
              <div style="padding-bottom: {{ image.space }}"></div>
            </div>
            <noscript>
              <img src="{{ image.url }}" alt="">
            </noscript>

     */

    var MAIN_ATTRS = ['src', 'srcset'];        // свойства, начинающие загрузку файла
    var SECONDARY_ATTRS = ['sizes', 'alt', 'width', 'height', 'class'];

    // Выборка значений ключей names из data или атрибутов
    var getAttrs = function($elem, names) {
        var result = {};
        var data = $elem.data();
        for (var i = 0, l = names.length; i < l; i++) {
            var name = names[i];

            var value = data[name];
            if (!value) {
                value = $elem.attr(name);
            }

            if (value) {
                result[name] = value;
            }
        }
        return result;
    };

    $.fn.loadImage = function(callback) {
        return this.map(function() {
            var $this = $(this);
            if (!$this.hasClass('lazyload')) {
                return this;
            }

            var $img = $('<img>').attr(getAttrs($this, SECONDARY_ATTRS));

            $img.onLoaded(function() {
                $this.before($img).remove();
                $img.addClass('loaded').removeClass('lazyload');

                if ($.isFunction(callback)) {
                    callback.call($img.get(0));
                }
            });

            $img.attr(getAttrs($this, MAIN_ATTRS));
            return $img;
        });
    };

    $(document).ready(function() {
        $.visibilityInspector.inspect('.lazyload.onview', {
            afterCheck: function($elem, opts, state) {
                if (state) {
                    $elem.loadImage();
                    this.ignore($elem);
                }
            }
        });
    });

})(jQuery);
