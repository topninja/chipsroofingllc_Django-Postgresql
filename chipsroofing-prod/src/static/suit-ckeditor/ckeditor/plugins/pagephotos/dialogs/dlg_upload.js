(function($) {

    /** @namespace editor.config.PAGEPHOTOS_THUMB_SIZE */
    /** @namespace editor.config.PAGEPHOTOS_UPLOAD_URL */
    /** @namespace editor.config.PAGEPHOTOS_MAX_FILE_SIZE */
    
    var InitPluploader = function(editor) {
        $(".ckupload-page-photos").plupload({
            runtimes : 'html5,flash,silverlight,html4',
            url : editor.config.PAGEPHOTOS_UPLOAD_URL,
            max_file_size : editor.config.PAGEPHOTOS_MAX_FILE_SIZE,
            chunk_size: '256kb',
            file_data_name: 'image',
            headers: {
                'X-CSRFToken': $.cookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            filters : [
               {title : "Image files", extensions : "jpg,jpeg,gif,png,bmp,tif,tiff"}
            ],
            unique_names : true,
            prevent_duplicates: true,
            sortable: true,
            dragdrop: true,
            autostart: true,
            thumb_width: editor.config.PAGEPHOTOS_THUMB_SIZE[0],
            thumb_height: editor.config.PAGEPHOTOS_THUMB_SIZE[1],
            views: {
               list: false,
               thumbs: true,
               default: 'thumbs'
            },
            flash_swf_url : editor.config.MOXIE_SWF,
            silverlight_xap_url : editor.config.MOXIE_XAP,

            init: {
                BeforeUpload: function() {
                    var ckDialog = CKEDITOR.dialog.getCurrent();
                    ckDialog._.buttons['ok'].disable();
                    ckDialog._.buttons['cancel'].disable();
                },
                FileUploaded: function(up, file, data) {
                    var response = JSON.parse(data.response);
                    file.result_tag = response.tag;

                    // Записываем id сохраненных картинок в форму
                    var text_field = $('#id_' + response.field);
                    if (text_field.length) {
                        var pagephotos = text_field.siblings('input[name="' + response.field + '-page-photos"]');
                        if (!pagephotos.length) {
                            pagephotos = $('<input type="hidden" name="' + response.field + '-page-photos">');
                            text_field.before(pagephotos);
                        }

                        // Формируем список id загруженных картинок
                        var value = pagephotos.val() || '';
                        if (value) {
                            value += ',' + response.id
                        } else {
                            value = response.id
                        }

                        pagephotos.val(value);
                    }
                },
                UploadComplete: function(up, files) {
                    var ckDialog = CKEDITOR.dialog.getCurrent();
                    ckDialog._.buttons['ok'].enable();
                    ckDialog._.buttons['cancel'].enable();
                },
                Error: function(up, error) {
                    up.removeFile(error.file);
                    var $widget = $(".ckupload-page-photos");

                    if (error.response) {
                        try {
                            var response = JSON.parse(error.response);
                            $widget.plupload('notify', 'error', response.message);
                            return
                        } catch (e) {
                        }
                    }

                    $widget.plupload('notify', 'error', response.message);
                }
            }
        })
    };

    CKEDITOR.dialog.add("pagephotosDialog", function (editor) {
        var lang = editor.lang.pagephotos;
        return {
            title: lang.dialogTitle,
            minWidth: 700,
            minHeight: 400,
            resizable: false,
            contents: [{
                id: 'tab-basic-photos',
                label: 'Basic Settings',
                elements: [{
                    type: 'html',
                    html: '<div class="ckupload-files ckupload-page-photos">' + lang.loading + '</div>'
                }]
            }],
            onLoad: function() {
                this.getElement().addClass('ckupload_dialog');

                // CSS приходится грузить JS-ом из-за переопределения стилей
                if (editor.config.PLUPLOADER_CSS) {
                    for (var i=0, l=editor.config.PLUPLOADER_CSS.length; i<l; i++) {
                        CKEDITOR.document.appendStyleSheet(editor.config.PLUPLOADER_CSS[i])
                    }
                }

                // Инициализация загрузчика
                InitPluploader(editor);
            },
            onOk: function() {
                var uploader = $('.ckupload-page-photos'),
                    uploaded=[],
                    not_loaded = [],
                    file,
                    img,
                    file_index,
                    tag_index;

                // Очистка очереди и получение тегов изображений
                var files = uploader.plupload('getFiles');
                for (file_index=files.length-1; file_index>=0; file_index--) {
                    file = files[file_index];
                    if (file.status === 1) {
                        not_loaded.push(file);
                    } else {
                        if (file.status === 5) {
                            uploaded.push(file.result_tag.trim());
                        }

                        uploader.plupload('removeFile', file)
                    }
                }

                if (not_loaded.length) {
                    var need_load = confirm(lang.unUploaded);

                    if (need_load) {
                        uploader.plupload('start');
                        return false
                    }
                }

                if (uploaded.length) {
                    // Вставка картинок
                    var output;
                    var container = editor.getSelection().getStartElement();
                    if (container.hasClass('page-images')) {
                        for (tag_index = uploaded.length - 1; tag_index >= 0; tag_index--) {
                            output = CKEDITOR.dom.element.createFromHtml(uploaded[tag_index], editor.document);
                            editor.insertElement(output);
                        }
                    } else {
                        container = editor.document.createElement('p');
                        container.addClass('page-images');
                        for (tag_index = uploaded.length - 1; tag_index >= 0; tag_index--) {
                            output = CKEDITOR.dom.element.createFromHtml(uploaded[tag_index], editor.document);
                            container.append(output)
                        }
                        editor.insertElement(container)
                    }

                    // Определение типа галереи
                    if (container.getElementsByTag('img').count() > 1) {
                        container
                            .removeClass('single-image')
                            .addClass('multi-image')
                    } else {
                        container
                            .removeClass('multi-image')
                            .addClass('single-image')
                    }
                }
            },

            onCancel: function() {
                // Очистка очереди
                var $uploader = $('.ckupload-page-photos');
                var files = $uploader.plupload('getFiles');
                for (var file_index=files.length-1; file_index>=0; file_index--) {
                    $uploader.plupload('removeFile', files[file_index])
                }
            }
        }
    })

})(jQuery);
