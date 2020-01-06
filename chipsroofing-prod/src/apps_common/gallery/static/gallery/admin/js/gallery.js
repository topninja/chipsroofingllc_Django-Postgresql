(function($) {

    /** @namespace gettext */

    $(document).ready(function() {
        $('.gallery-standart').each(function() {
            if (!$(this).closest('.empty-form').length) {
                DefaultGallery(this);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('gallery', function(inline_prefix, row) {
                $(row).find('.gallery-standart').each(function() {
                    DefaultGallery(this);
                });
            });
        }
    }).on('click.gallery', '.create-gallery', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        $button.prop('disabled', true);
        gallery.createGallery().always(function() {
            $button.prop('disabled', false);
        });

        return false;
    }).on('click.gallery', '.delete-gallery', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        if (!confirm(gettext('Are you sure you want to delete this gallery?'))) {
            return false
        }

        $button.prop('disabled', true);
        gallery.deleteGallery().always(function() {
            $button.prop('disabled', false);
        });

        return false;
    }).on('click.gallery', '.add-gallery-video', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var video_link = prompt(gettext('Paste YouTube/Vimeo video URL'), 'http://');
        if (video_link) {
            gallery.addVideo(video_link);
        }

        return false;
    }).on('click.gallery', '.item-delete', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.deleteItem($item);

        return false;
    }).on('click.gallery', '.item-rotate-left', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.rotateItem($item, 'left').done(function() {
            $item.find('.item-crop').removeData('crop').removeAttr('data-crop');
        });

        return false;
    }).on('click.gallery', '.item-rotate-right', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.rotateItem($item, 'right').done(function() {
            $item.find('.item-crop').removeData('crop').removeAttr('data-crop');
        });

        return false;
    });

    /*
        Дополнительная форма к элементу галереи
     */
    $(document).on('click.gallery', '.item-form', function() {
        var $button = $(this);
        var gallery = $button.closest('.gallery').data(Gallery.prototype.DATA_KEY);
        if (!gallery) {
            console.error('Gallery object not found');
            return false;
        }

        var $item = $button.closest('.gallery-item');
        gallery.getItemForm($item).done(function(response) {
            var $template = $(response.html);
            $template.dialog({
                dialogClass: "edit-item-dialog",
                title: gettext('Edit item'),
                width: 460,
                closeText: '',
                show: {
                    effect: "fadeIn",
                    duration: 100
                },
                hide: {
                    effect: "fadeOut",
                    duration: 100
                },
                modal: true,
                draggable: false,
                resizable: false,
                position: {
                    my: "center center",
                    at: "center center",
                    of: window
                },
                buttons: [
                    {
                        text: gettext('Cancel'),
                        "class": 'btn',
                        icons: {
                            primary: "ui-icon-cancel"
                        },
                        click: function() {
                            $(this).dialog('close');
                        }
                    },
                    {
                        text: gettext('Ok'),
                        "class": 'ok-btn btn btn-info',
                        icons: {
                            primary: "ui-icon-check"
                        },
                        click: function() {
                            var $form = $(this);
                            var dialog = $form.dialog('instance');

                            var item, i=0;
                            var data = {};
                            var form_data = $form.serializeArray();
                            while (item = form_data[i++]) {
                                data[item.name] = item.value;
                            }

                            dialog.uiDialog.addClass('preloader');
                            gallery.saveItemForm($item, data, function(response) {
                                /** @namespace response.errors.fullname */

                                if (response.errors) {
                                    var record = response.errors[0];
                                    $form.find('.' + record.fullname).addClass(record.class);
                                    alert(record.errors[0]);
                                }
                            }).done(function() {
                                $form.dialog('close');
                            }).always(function() {
                                dialog.uiDialog.removeClass('preloader');
                            });
                        }
                    }
                ],
                open: function() {
                    var $form = $(this);
                    var dialog = $form.dialog('instance');

                    // отправка формы
                    $form.on('submit', function() {
                        dialog.uiDialog.find('.ok-btn').click();
                        return false;
                    });

                    if ($.fn.autosize) {
                        $form.find('textarea').autosize({
                            callback: function() {
                                if (dialog.widget().outerHeight() < $.winHeight()) {
                                    dialog._position();
                                }
                            }
                        });
                    }
                },
                close: function() {
                    $(this).dialog('destroy');
                }
            });
        });

        return false;
    });

})(jQuery);
