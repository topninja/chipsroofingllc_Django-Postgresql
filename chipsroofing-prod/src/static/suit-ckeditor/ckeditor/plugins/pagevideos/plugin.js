(function() {

    CKEDITOR.plugins.add("pagevideos", {
        icons: 'pagevideos',
        lang: 'en,ru',
        init: function (editor) {
            var lang = editor.lang.pagevideos;
            editor.addContentsCss(this.path + 'styles/editor.css');
            CKEDITOR.scriptLoader.load(
                CKEDITOR.getUrl(this.path + 'libs/jquery.oembed.js')
            );

            // ======================================
            //      Dialogs
            // ======================================
            CKEDITOR.dialog.add('pagevideosDialog', this.path + 'dialogs/dlg_upload.js');
            CKEDITOR.dialog.add('pagevideos_block_description', this.path + 'dialogs/block_description.js');

            // ======================================
            //      Commands
            // ======================================

            // UPLOAD
            editor.addCommand('pagevideos', new CKEDITOR.dialogCommand('pagevideosDialog', {
                allowedContent: 'p(!page-video);p[!data-url];p iframe[*]'
            }));

            // BLOCK DESCRIPTION
            editor.addCommand('pagevideos_block_description', new CKEDITOR.dialogCommand('pagevideos_block_description'));

            // CHANGE VIDEO
            editor.addCommand('ChangeVideo', {
                exec: function (editor) {
                    editor.openDialog('pagevideosDialog')
                },
                canUndo: false
            });


            // ======================================
            //      Context menu
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('pageVideo', 150);
            editor.addMenuItems({
                _change_video : {
                    label : lang.contextMenuEdit,
                    icon: this.path + 'icons/edit.png',
                    command : 'ChangeVideo',
                    group : 'pageVideo',
                    order: 10
                },
                _video_block_description : {
                    label : lang.contextMenuBlockDescr,
                    icon: this.path + 'icons/descr.png',
                    command : 'pagevideos_block_description',
                    group : 'pageVideo',
                    order: 20
                }
            });
            editor.contextMenu.addListener(function (element) {
                if (element && element.hasClass('page-video')) {
                    return {
                        _change_video : CKEDITOR.TRISTATE_OFF,
                        _video_block_description : CKEDITOR.TRISTATE_OFF
                    }
                }

                return null
            });

            // ======================================
            //      Buttons
            // ======================================
            editor.ui.addButton('PageVideos', {
                label: lang.buttonTitle,
                command: 'pagevideos',
                toolbar: 'insert'
            });


            editor.on('contentDom', function () {
                // Удаление контейнера при удалении видео через Backspace и Delete
                editor.on('key', function (evt) {
                    if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                        if (editor.mode !== "wysiwyg") {
                            return
                        }

                        // if we call getStartElement too soon, we get the wrong element
                        setTimeout(function () {
                            var container = editor.getSelection().getStartElement();
                            if (container.hasClass('page-video')) {
                                if (container.getElementsByTag('iframe').count() === 0) {
                                    container.remove()
                                }
                            }
                        }, 10)
                    }
                })
            })
        }
    })

})();
