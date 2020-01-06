(function() {

    CKEDITOR.plugins.add("pagefiles", {
        requires: 'file_widget',
        icons: 'pagefiles',
        lang: 'en,ru',
        init: function(editor) {
            var lang = editor.lang.pagefiles;
            editor.addContentsCss(this.path + 'styles/editor.css');

            // ======================================
            //      Dialogs
            // ======================================
            CKEDITOR.dialog.add("pagefilesDialog", this.path + "dialogs/dlg_upload.js");

            // ======================================
            //      Commands
            // ======================================
            editor.addCommand("pagefiles", new CKEDITOR.dialogCommand("pagefilesDialog", {
                allowedContent: 'div(!page-file)[!data-id]; span'
            }));

            // ======================================
            //      Buttons
            // ======================================
            editor.ui.addButton("PageFiles", {
                label: lang.buttonTitle,
                command: "pagefiles",
                toolbar: 'insert'
            });

            editor.on('key', function(evt) {
                if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                    if (editor.mode !== "wysiwyg") {
                        return
                    }

                    // if we call getStartElement too soon, we get the wrong element
                    setTimeout(function() {
                        var containers = editor.document.find('.page-files');
                        for (var i = 0, container; container = containers.getItem(i); i++) {
                            if (!container.getChildCount()) {
                                container.remove();
                            }
                        }
                    }, 10)
                }
            }, null, null, 8);
        }
    })

})();
