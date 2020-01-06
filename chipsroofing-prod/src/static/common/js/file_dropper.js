(function($) {
    'use strict';

    /*
        Обработчик перетаскивания файлов.

        Требует:
            jquery.utils.js

        Параметры:
            dragOverClass   - класс, который вешается на DOM-элемент
                              при перетаскивании над ним файла
            preventDrop     - предотвращать поведение drop по умолчанию

        События:
            dragstart       - начало перетаскивания над областью
            dragend         - завершение перетаскивания над областью
            drop            - файлы переместили на область

     */
    window.FileDropper = Class(EventedObject, function FileDropper(cls, superclass) {
        cls.defaults = {
            dragOverClass: 'dragover',
            preventDrop: false
        };

        cls.DATA_KEY = 'file_dropper';


        cls.init = function(root, options) {
            superclass.init.call(this);

            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            var that = this;
            var drag_counter = 0;
            this.$root.on('dragenter.file_dropper', function() {
                drag_counter++;
                if (drag_counter === 1) {
                    $(this).addClass(that.opts.dragOverClass);

                    // callback
                    that.trigger('dragstart');
                }
            }).on('dragstart.file_dropper', function() {
                return false;
            }).on('dragover.file_dropper', function() {
                return false;
            }).on('dragleave.file_dropper', function() {
                drag_counter--;
                if (drag_counter === 0) {
                    $(this).removeClass(that.opts.dragOverClass);

                    // callback
                    that.trigger('dragend');
                }
            }).on('drop.file_dropper', function(event) {
                drag_counter = 0;

                // callback
                that.trigger('dragend');

                var files = that.getFiles(event.originalEvent.dataTransfer);
                if (files.length) {
                    that.trigger('drop', files);
                }

                setTimeout(function() {
                    that.$root.removeClass(that.opts.dragOverClass);
                }, 0);

                if (that.opts.preventDrop) {
                    return false;
                }
            });

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$root.off('.file_dropper');
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        /*
            Получение переданных файлов
         */
        cls.getFiles = function(transfer) {
            if (!transfer) {
                this.warn('no transfer');
                return [];
            }

            var files = transfer.files;
            if (!files.length) {
                this.warn('no files');
                return [];
            }

            return files;
        }
    });

})(jQuery);