(function($) {

    /*
        Виджет поля файла с превью.

        Требует:
            jquery.utils.js
            file_dropper.js

        Параметры:
            previewsSelector    - селектор контейнера с превью
            oldPreviewSelector  - селектор исходного превью
            newPreviewSelector  - селектор нового превью

            emptyClass          - класс, который вешается на обертку в случае,
                                  когда на бэкенде и фронтенде нет значения
            dragOverClass       - класс, который вешается на обертку при
                                  перетаскивании файла над полем
            preloaderClass      - класс, который вешается на обертку при
                                  загрузке файла перед генерацией нового превью
     */
    window.StdImage = Class(Object, function StdImage(cls, superclass) {
        cls.defaults = {
            previewsSelector: '.previews',
            oldPreviewSelector: '.old-preview',
            newPreviewSelector: '.new-preview',

            emptyClass: 'empty',
            dragOverClass: 'dragover',
            preloaderClass: 'preloader'
        };

        cls.DATA_KEY = 'stdimage';


        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            this.$input = this.$root.find('input[type="file"]');
            if (!this.$input.length) {
                return this.raise('input element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // превью
            this.$previews = this.$root.find(this.opts.previewsSelector);
            this.$old_preview = this.$root.find(this.opts.oldPreviewSelector);
            this.$new_preview = this.$root.find(this.opts.newPreviewSelector);

            // значение не установлено изначально
            this._wasEmpty = this.$root.hasClass(this.opts.emptyClass) || !this.$old_preview.length;

            // обработчик перетаскивания файлов
            this.dropper = FileDropper(this.$root, {
                dragOverClass: this.opts.dragOverClass
            });

            // Изменение файла
            var that = this;
            this.$input.on('change.stdimage', function() {
                that.changeHandler($(this));
            });

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.dropper.destroy();
            this.$root.off('.stdimage');
            this.$input.off('.stdimage');
            this.$root.removeData(this.DATA_KEY);
        };

        /*
            Сброс на первоначальное превью, если оно было
         */
        cls.resetPreview = function() {
            this.$new_preview.removeAttr('src').hide();
            if (this._wasEmpty) {
                this.$root.addClass(this.opts.emptyClass);
            } else {
                this.$old_preview.show();
            }
        };

        /*
            Создание нового превью
         */
        cls.setPreview = function(img) {
            // размер превью
            var size = this.$root.data('size').toString()
                .split('x').map(function(item) {
                    return parseInt(item)
                }).filter(Boolean);
            if (size.length !== 2) {
                size = [this.$previews.width(), this.$previews.height()];
            }

            // создаем превью
            var final_canvas = $.previewCanvas({
                source: img,
                width: size[0],
                height: size[1],
                crop: true,
                stretch: false
            });

            this.$root.removeClass(this.opts.emptyClass);
            this.$root.removeClass(this.opts.preloaderClass);

            this.$old_preview.hide();
            this.$new_preview.attr('src', final_canvas.toDataURL()).show();
        };

        /*
            Событие изменения файла
         */
        cls.changeHandler = function($input) {
            var file = $input.prop('files');
            file = file && file.length && file[0];
            if (!file) {
                this.resetPreview();
                return;
            }

            this.$root.addClass(this.opts.preloaderClass);

            var that = this;
            $.fileReaderDeferred(file).done(function(src) {
                $.loadImageDeferred(src).done(function(img) {
                    src = null;
                    that.setPreview(img);
                }).fail(function() {
                    that.resetPreview();
                    that.$root.removeClass(that.opts.preloaderClass);
                })
            }).fail(function() {
                that.resetPreview();
                that.$root.removeClass(that.opts.preloaderClass);
            });
        };
    });


    $(document).ready(function() {
        $('.stdimage').each(function() {
            window.StdImage(this);
        })
    })

})(jQuery);