(function($) {
    'use strict';

    /*
        Класс галереи, предоставляющий базовые методы работы над картинками.

        События:
            create.gallery      - галерея создана
            init.gallery        - галерея инициализирована
            delete.gallery      - галерея удалена
            destroy.gallery     - освобождение ресурсов JS-объекта галереи
            item-add.gallery    - добавлен новый элемент
            item-error.gallery  - ошибка добавления элемента
            item-delete.gallery - элемент удален из галереи

    */

    /** @namespace gettext */
    /** @namespace ngettext */
    /** @namespace interpolate */

    var formatError = function(message) {
        return gettext('Error') + ':<br>' + message;
    };

    window.Gallery = Class(EventedObject, function Gallery(cls, superclass) {
        cls.defaults = {
            galleryInputSelector: '.gallery_id',
            galleryWrapperSelector: '.gallery-wrapper',
            galleryListSelector: '.gallery-items',

            uploadButtonSelector: '.add-gallery-image',

            previewSelector: '.item-preview',
            preloaderSelector: '.item-preloader',
            progressSelector: '.progress',
            progressBarSelector: '.progress-bar',
            controlsSelector: '.item-controls',

            imageTemplateSelector: '.image-template',
            videolinkTemplateSelector: '.videolink-template',

            loadingClass: 'gallery-item-loading',
            errorClass: 'gallery-item-error'
        };

        cls.DATA_KEY = 'gallery';


        cls.init = function(root, options) {
            superclass.init.call(this);

            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // данные о галерее
            this.app_label = this.$root.data('applabel');
            if (!this.app_label) {
                return this.raise('app_label reqired');
            }

            this.model_name = this.$root.data('modelname');
            if (!this.model_name) {
                return this.raise('model_name reqired');
            }

            this.$galleryInput = this.$root.find(this.opts.galleryInputSelector).first();
            if (!this.$galleryInput.length) {
                return this.raise('input element not found');
            }

            this.field_name = this.$galleryInput.attr('name');
            if (!this.field_name) {
                return this.raise('field_name required');
            }

            this.$wrapper = this.$root.find(this.opts.galleryWrapperSelector).first();
            if (!this.$wrapper.length) {
                return this.raise('wrapper element not found');
            }

            this._locked = false;
            this.gallery_id = null;
            this.$list = $();

            // инициализация галереи
            var gallery_id = parseInt(this.$galleryInput.val()) || null;
            if (gallery_id) {
                this.initGallery(gallery_id);
            }

            this.$root.data(this.DATA_KEY, this);

            // event
            this.trigger('create.gallery');
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // event
            this.trigger('destroy.gallery');

            if (this.dropper) {
                this.dropper.destroy();
            }
            if (this.uploader) {
                this.uploader.destroy();
            }
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        cls.locked = function() {
            return this._locked;
        };

        cls.lock = function() {
            this._locked = true;
        };

        cls.unlock = function() {
            this._locked = false;
        };

        /*
            Базовая обертка над AJAX-запросами
         */
        cls.ajax = function(options) {
            var that = this;
            var opts = $.extend(true, {
                type: 'POST',
                data: {
                    app_label: this.app_label,
                    model_name: this.model_name,
                    field_name: this.field_name,
                    gallery_id: this.gallery_id
                },
                dataType: 'json',
                beforeSend: function() {
                    that.lock();
                },
                error: $.parseError(),
                complete: function() {
                    that.unlock();
                }
            }, options);

            return $.ajax(opts);
        };

        /*
            Базовая обертка над AJAX-запросами для элемента галереи
         */
        cls.ajaxItem = function($item, options) {
            var that = this;
            var item = $item.get(0);

            var item_id = parseInt($item.data('id')) || 0;
            if (!item_id) {
                return $.Deferred();
            }

            if (item.query) {
                item.query.abort();
            }
            var opts = $.extend(true, {
                type: 'POST',
                data: {
                    app_label: this.app_label,
                    model_name: this.model_name,
                    field_name: this.field_name,
                    gallery_id: this.gallery_id,
                    item_id: item_id
                },
                dataType: 'json',
                beforeSend: function() {
                    $item.addClass(that.opts.loadingClass);
                },
                error: $.parseError(),
                complete: function() {
                    $item.removeClass(that.opts.loadingClass);
                }
            }, options);

            return item.query = $.ajax(opts);
        };

        /*
            Создание галереи
         */
        cls.createGallery = function() {
            if (this.locked()) {
                return
            }

            if (this.gallery_id) {
                this.error('gallery already exists for this entry');
                return;
            }

            var that = this;
            return this.ajax({
                url: window.admin_gallery_create,
                success: function(response) {
                    that.$wrapper.html(response.html);
                    that.initGallery(response.gallery_id);
                },
                error: $.parseError()
            });
        };

        /*
            Инициализация галереи
         */
        cls.initGallery = function(gallery_id) {
            gallery_id = parseInt(gallery_id);
            if (!gallery_id) {
                this.error('invalid gallery_id');
                return;
            }

            this.gallery_id = gallery_id;
            this.$galleryInput.val(gallery_id);

            // список файлов
            this.$list = this.$root.find(this.opts.galleryListSelector).first();
            if (!this.$list.length) {
                this.error('items container not found');
                return;
            }

            this.updateCounter();

            this.initUploader();

            // перемещение файлов
            var that = this;
            this.dropper = FileDropper(this.$wrapper, {
                preventDrop: true
            }).on('drop', function(files) {
                if (!that.uploader) {
                    return
                }

                var i = 0;
                var file;
                while (file = files[i++]) {
                    that.uploader.addFile(file);
                }
            });

            // event
            setTimeout(function() {
                that.trigger('init.gallery');
            }, 0);
        };

        /*
            Инициализация загрузчика файлов
         */
        cls.initUploader = function() {
            // Клиентский ресайз
            var resize = this.$root.find('.max_source').val();
            if (resize) {
                resize = String(resize).split('x').map(function(e) {
                    return parseInt(e)
                });
                resize = canvasSize(Math.max(resize[0], 100), Math.max(resize[1], 100));
            } else {
                resize = {};
            }

            // Максимальный вес
            var max_size = this.$root.find('.max_size').val();
            max_size = Number(max_size) || 0;

            var that = this;
            that.uploader = Uploader(this.$root, {
                url: window.admin_gallery_upload,
                buttonSelector: this.opts.uploadButtonSelector,
                drop_element: 'self',
                resize: resize,
                max_size: max_size,

                getExtraData: function() {
                    return {
                        app_label: that.app_label,
                        model_name: that.model_name,
                        field_name: that.field_name,
                        gallery_id: that.gallery_id
                    }
                },
                onFileAdded: function(file) {
                    var template = that.$root.find(that.opts.imageTemplateSelector).html();
                    var $item = $(template);
                    $item.attr('id', file.id);
                    that.$list.append($item);

                    return that._checkMaxItemCount($item);
                },
                onBeforeFileUpload: function(file) {
                    var $item = that.$list.find('#' + file.id);
                    $item.addClass(that.opts.loadingClass);
                },
                onFileUploadProgress: function(file, percent) {
                    var $item = that.$list.find('#' + file.id);
                    $item.find(that.opts.progressBarSelector).css({
                        width: percent + '%'
                    });
                },
                onFileUploaded: function(file, json_response) {
                    /** @namespace json_response.show_url */
                    /** @namespace json_response.preview_url */

                    var $item = that.$list.find('#' + file.id);
                    var $preview = $item.find(that.opts.previewSelector);

                    $item.removeClass(that.opts.loadingClass);
                    $item.data({
                        id: json_response.id,
                        source_url: json_response.source_url,
                        source_size: json_response.source_size
                    });

                    $preview.attr('href', json_response.show_url);

                    // Загрузка реального превью
                    $.loadImageDeferred(json_response.preview_url).done(function(img) {
                        $preview.show();
                        $preview.find('img').attr('src', img.src);
                        $item.find(that.opts.preloaderSelector).remove();
                    }).fail(function(reason) {
                        that.error(reason);
                    });

                    // event
                    that.trigger('item-add.gallery', $item, json_response);
                },
                onUploadComplete: function() {
                    that.updateCounter();
                },
                onFileUploadError: function(file, error, json_response) {
                    var $item = that.$list.find('#' + file.id);
                    var $preview = $item.find(that.opts.previewSelector);

                    var $controls = $item.find(that.opts.controlsSelector);
                    $controls.hide();

                    // Ошибка показывается на фоне превью
                    $.fileReaderDeferred(file.getNative()).done(function(src) {
                        $.loadImageDeferred(src).done(function(img) {
                            src = null;
                            $.imageToCanvasDeferred(img, 600, 600).done(function(canvas) {
                                img = null;

                                var $image = $('<img>');
                                $preview.find('img').remove();
                                $preview.prepend($image).css({
                                    background: 'none'
                                });

                                var final_canvas = $.previewCanvas({
                                    source: canvas,
                                    width: $preview.width(),
                                    height: $preview.height(),
                                    crop: true,
                                    stretch: false
                                });
                                $image.attr('src', final_canvas.toDataURL());
                            });
                        });
                    });

                    $controls.show();

                    var error_msg = (json_response && json_response.message) || (error && error.message);
                    that.setItemError($item, error_msg);

                    // event
                    that.trigger('item-error.gallery', $item, json_response);
                }
            });
        };

        /*
            Проверка максимального кол-ва элементов
         */
        cls._checkMaxItemCount = function($item) {
            // проверка максимального кол-ва элементов
            var max_count = this.$root.find('.max_item_count').val();
            max_count = parseInt(max_count) || 0;
            if (max_count > 0) {
                var $items = this.$list.find('.gallery-item');
                $items = $items.not('.' + this.opts.errorClass);
                if ($items.length > max_count) {
                    var err_msg = ngettext(
                        'this gallery can\'t contain more than %s item',
                        'this gallery can\'t contain more than %s items',
                        max_count
                    );
                    this.setItemError($item, interpolate(err_msg, [max_count]));
                    return false;
                }
            }
            return true;
        };

        /*
            Установка ошибки на элементе галереи
         */
        cls.setItemError = function($item, message) {
            $item.removeClass(this.opts.loadingClass);
            $item.addClass(this.opts.errorClass);
            $item.find(this.opts.progressSelector).remove();

            if (message) {
                var $preview = $item.find(this.opts.previewSelector);
                $preview.append(
                    $('<span>').html(formatError(message))
                );
                $preview.show();
            }
        };

        /*
            Обновление значения счетчиков картинок
         */
        cls.updateCounter = function() {
            var $img_counter = this.$root.find('.gallery-image-counter');
            if ($img_counter.length) {
                var $images = this.$list.find('.gallery-item-image');
                $images = $images.not('.' + this.opts.errorClass);
                $images = $images.not('.' + this.opts.loadingClass);
                $img_counter.text($images.length);
            }

            var $video_counter = this.$root.find('.gallery-videolink-counter');
            if ($video_counter.length) {
                var $videos = this.$list.find('.gallery-item-video-link');
                $videos = $videos.not('.' + this.opts.errorClass);
                $videos = $videos.not('.' + this.opts.loadingClass);
                $video_counter.text($videos.length);
            }
        };

        /*
            Удаление галереи
         */
        cls.deleteGallery = function() {
            if (this.locked()) {
                return
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            var that = this;
            return this.ajax({
                url: window.admin_gallery_delete,
                success: function(response) {
                    that.gallery_id = null;
                    that.$galleryInput.val('');

                    that.dropper.destroy();
                    that.uploader.destroy();
                    that.$list = $();

                    that.updateCounter();

                    that.$wrapper.html(response.html);

                    // event
                    that.trigger('delete.gallery');
                },
                error: $.parseError()
            });
        };

        /*
            Добавление ссылки на видео
         */
        cls.addVideo = function(link) {
            if (this.locked()) {
                return;
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            var template = this.$root.find(this.opts.videolinkTemplateSelector).html();
            var $item = $(template);
            this.$list.append($item);

            // проверка максимального кол-ва
            if (!this._checkMaxItemCount($item)) {
                return;
            }

            var that = this;
            return this.ajax({
                url: window.admin_gallery_upload_video,
                data: {
                    link: link
                },
                beforeSend: function() {
                    $item.addClass(that.opts.loadingClass);
                },
                success: function(response) {
                    var $preview = $item.find(that.opts.previewSelector);

                    $item.data({
                        id: response.id
                    });

                    $preview.attr('href', response.show_url);

                    // Загрузка реального превью
                    $.loadImageDeferred(response.preview_url).done(function(img) {
                        $preview.show();
                        $preview.find('img').attr('src', img.src);
                        $item.find(that.opts.preloaderSelector).remove();
                    }).fail(function(reason) {
                        that.error(reason);
                    });

                    that.updateCounter();

                    // event
                    that.trigger('item-add.gallery', $item, response);
                },
                error: $.parseError(function(response) {
                    var $preview = $item.find(that.opts.previewSelector);
                    $item.addClass(that.opts.errorClass);
                    $preview.show();

                    if (response && response.message) {
                        $preview.append(
                            $('<span>').html(response.message)
                        );
                    }

                    // event
                    that.trigger('item-error.gallery', $item, response);
                }),
                complete: function() {
                    $item.removeClass(that.opts.loadingClass);
                }
            })
        };

        /*
            Удаление элемента галереи
         */
        cls.deleteItem = function($item) {
            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            if (!$item.length) {
                this.error('item element not found');
                return;
            }

            // Удаление элемента галереи из очереди загрузок
            if (this.uploader && this.uploader.uploader) {
                this.uploader.removeFile($item.attr('id'));
            }

            // Если еще не загружен - удаляем
            var that = this;
            var item_id = parseInt($item.data('id')) || 0;
            if (!item_id || $item.hasClass(this.opts.loadingClass) || $item.hasClass(this.opts.errorClass)) {
                // Удаление блока из DOM
                var df = $.Deferred();
                $item.animate({
                    height: 0,
                    width: 0
                }, {
                    duration: 100,
                    complete: function() {
                        df.resolve();

                        // event
                        that.trigger('item-delete.gallery', $item);

                        $item.remove();
                    }
                });
                return df.promise();
            } else {
                return this.ajaxItem($item, {
                    url: window.admin_gallery_delete_item,
                    success: function() {
                        // Удаление блока из DOM
                        $item.animate({
                            height: 0,
                            width: 0
                        }, {
                            duration: 100,
                            complete: function() {
                                $item.remove();
                                // event
                                that.trigger('item-delete.gallery', $item);

                                that.updateCounter();
                            }
                        })
                    }
                })
            }
        };

        /*
            Поворот картинки
         */
        cls.rotateItem = function($item, direction) {
            if (this.locked()) {
                return
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            if (!$item.length) {
                this.error('item element not found');
                return;
            }

            direction = direction || 'left';

            return this.ajaxItem($item, {
                url: window.admin_gallery_rotate_item + '?direction=' + direction,
                success: function(response) {
                    $item.data({
                        source_url: response.source_url
                    }).find('img').attr({
                        src: response.preview_url
                    });
                }
            });
        };

        /*
            Обрезка картинки
         */
        cls.cropItem = function($item, coords, extra) {
            if (this.locked()) {
                return
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            if (!$item.length) {
                this.error('item element not found');
                return;
            }

            var data = $.extend({}, extra, {
                coords: coords
            });

            return this.ajaxItem($item, {
                url: window.admin_gallery_crop_item,
                data: data,
                success: function(response) {
                    $item.find('img').attr({
                        src: response.preview_url
                    });
                }
            });
        };

        /*
            Получение формы к элементу галереи
         */
        cls.getItemForm = function($item, extra) {
            if (this.locked()) {
                return
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            if (!$item.length) {
                this.error('item element not found');
                return;
            }

            var data = $.extend({}, extra);

            return this.ajaxItem($item, {
                url: window.admin_gallery_edit_item,
                type: 'get',
                async: false,
                data: data
            });
        };

        /*
            Установка подписи к картинке
         */
        cls.saveItemForm = function($item, data, error_callback) {
            if (this.locked()) {
                return
            }

            if (!this.gallery_id) {
                this.error('gallery_id required');
                return;
            }

            if (!$item.length) {
                this.error('item element not found');
                return;
            }

            return this.ajaxItem($item, {
                url: window.admin_gallery_edit_item,
                async: false,
                data: data,
                error: $.parseError(error_callback)
            });
        };
    });

})(jQuery);
