(function() {
    CKEDITOR.plugins.add("image_attrs", {
        requires: 'dialog',
        lang: 'en,ru',
        init: function (editor) {
            var lang = editor.lang.image_attrs;

            // ======================================
            //      Dialog
            // ======================================
            CKEDITOR.dialog.add("imageAttrsDialog", this.path + "dialogs/image_attrs.js");

            // ======================================
            //      Commandes
            // ======================================
            editor.addCommand('imageAttrs', new CKEDITOR.dialogCommand('imageAttrsDialog'));


            // ======================================
            //      Context Menu
            // ======================================
            if (editor.contextMenu) {
                editor.addMenuGroup('imageGroup', 110);
                editor.addMenuItem('imageAttrsItem', {
                    label: lang.menuTitle,
                    icon: this.path + 'icons/image_attrs.png',
                    command: 'imageAttrs',
                    group: 'imageGroup',
                    order: 10
                });

                editor.contextMenu.addListener(function(element) {
                    if (element && element.is('img') && !element.isReadOnly()) {
                        return {
                            imageAttrsItem: CKEDITOR.TRISTATE_OFF
                        }
                    }
                });
            }
        }
    })

})();
