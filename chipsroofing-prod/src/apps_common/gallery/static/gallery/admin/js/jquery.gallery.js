(function($) {

    /*
        Галерея, добавляющая возможность выделения элементов галереи,
        их массовое удаление, сортировку, обрезку картинки.
     */
    window.DefaultGallery = Class(Gallery, function DefaultGallery(cls, superclass) {
        cls.init = function(root, options) {
            superclass.init.call(this, root, options);

            this.on('init.gallery', function() {
                this.initCropdialog();
                this.initSortable();
                this.initChecking();
                this.initMassDelete();
            }).on('destroy.gallery', function() {
                if (this.cropdialog) {
                    this.cropdialog.destroy();
                }
                this.$list.sortable('destroy');
                this.$list.off('.checkitem');
                this.$root.off('.massdelete');
            }).on('item-add.gallery', function($item, response) {
                // установка ссылки на просмотр полноразмерной картинки
                if (response && response.show_url) {
                    $item.find('.item-preview').attr('href', response.show_url);
                }
                $item.find('.check-box').val(response.id);
            }).on('item-delete.gallery', function() {
                // обновление состояния кнопки массового удаления
                this.checkChecked();
            });
        };

        /*
            Проверка наличия выделенных картинок. Если такие есть - включаем
            кнопку удаления выделенных элементов
         */
        cls.checkChecked = function() {
            var $checked = this.$list.find('.gallery-item-checked');
            this.$root.find('.delete-checked-items').prop('disabled', $checked.length === 0);
        };

        /*
            Инициализация диалогового окна для обрезки картинок
         */
        cls.initCropdialog = function() {
            var that = this;
            this.cropdialog = CropDialog(this.$root, {
                eventTypes: 'click.gallery.cropdialog',
                buttonSelector: '.gallery-item .item-crop',

                getImage: function($button) {
                    var $item = $button.closest('.gallery-item');
                    return $item.data('source_url');
                },
                getMinSize: function() {
                    return this.formatSize(that.$root.find('.min_dimensions').val());
                },
                getMaxSize: function() {
                    return this.formatSize(that.$root.find('.max_dimensions').val());
                },
                getAspects: function() {
                    return this.formatAspects(that.$root.find('.aspects').val());
                },
                getCropCoords: function($button) {
                    return this.formatCoords($button.data('crop'));
                },
                onCrop: function($button, coords) {
                    var coords_str = coords.join(':');
                    var $item = $button.closest('.gallery-item');
                    that.cropItem($item, coords_str);
                    $button.data('crop', coords_str);
                }
            });
        };

        /*
            Инициализация сортировки элементов
         */
        cls.initSortable = function() {
            var sort_query;

            var that = this;
            this.$list.sortable({
                containment: "parent",
                helper: 'clone',
                items: '> .gallery-item',
                tolerance: 'pointer',
                distance: 20,
                update: function() {
                    // Сохранение порядка файлов
                    var item_ids = [];
                    that.$root.find('.gallery-item').each(function() {
                        var item_id = parseInt($(this).data('id'));
                        if (item_id) {
                            item_ids.push(item_id)
                        }
                    });

                    if (sort_query) sort_query.abort();
                    sort_query = $.ajax({
                        url: window.admin_gallery_sort,
                        type: 'POST',
                        data: {
                            app_label: that.app_label,
                            model_name: that.model_name,
                            gallery_id: that.gallery_id,
                            item_ids: item_ids.join(',')
                        },
                        error: $.parseError(function(response) {
                            if (response && response.message) {
                                alert(response.message);
                            }
                        })
                    })
                }
            }).disableSelection();
        };

        /*
            Инициализация выделения элементов
         */
        cls.initChecking = function() {
            var that = this;
            this.$list.on('change.gallery.checkitem', '.check-box', function() {
                var $input = $(this);
                var $item = $input.closest('.gallery-item');

                if ($input.prop('checked')) {
                    $item.addClass('gallery-item-checked')
                } else {
                    $item.removeClass('gallery-item-checked')
                }

                that.checkChecked();
            });
        };

        /*
            Инициализация удаления выделенных элементов
         */
        cls.initMassDelete = function() {
            var that = this;
            this.$root.on('click.gallery.massdelete', '.delete-checked-items', function() {
                var $checked = that.$list.find('.gallery-item-checked');

                var confirm_fmt = ngettext(
                    'Are you sure you want to delete checked item?',
                    'Are you sure you want to delete %s checked items?',
                    $checked.length
                );
                if (!confirm(interpolate(confirm_fmt, [$checked.length]))) {
                    return false;
                }

                $checked.removeClass('.gallery-item-checked').each(function() {
                    that.deleteItem($(this));
                });

                that.checkChecked();

                return false;
            });
        };
    });

})(jQuery);
