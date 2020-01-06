(function() {

    CKEDITOR.plugins.add("file_widget", {
        requires: 'widget,dialog',
        icons: 'file_widget',
        lang: 'en,ru',
        init: function(editor) {
            var lang = editor.lang.file_widget;
            editor.addContentsCss(this.path + 'styles/editor.css');

            // ======================================
            //      Dialogs
            // ======================================
            CKEDITOR.dialog.add('fileDialog', this.path + 'dialogs/file_widget.js');

            // ======================================
            //      Widgets
            // ======================================
            editor.widgets.add('file_widget', {
                dialog: 'fileDialog',
                upcast: function(element) {
                    return element.hasClass('page-file')
                }
            });

            // ======================================
            //      Commands
            // ======================================
            editor.addCommand("file_widget_edit", new CKEDITOR.dialogCommand('fileDialog'));

            // ======================================
            //      Context Menu
            // ======================================
            if (editor.contextMenu) {
                editor.addMenuGroup('filesGroup');
                editor.addMenuItem('editFileItem', {
                    label: lang.contextMenuEdit,
                    icon: this.path + 'icons/edit.png',
                    command: 'file_widget_edit',
                    group: 'filesGroup'
                });

                editor.contextMenu.addListener(function(element) {
                    if (element && element.hasAttribute('data-cke-widget-id') && element.findOne('.page-file')) {
                        return {
                            editFileItem: CKEDITOR.TRISTATE_OFF
                        }
                    }
                });
            }


            editor.on('dragend', function(evt) {
                setTimeout(function() {
                    var widget = evt.editor.widgets.selected[0];
                    if (!widget || (widget.wrapper.type !== CKEDITOR.NODE_ELEMENT)) {
                        return
                    }

                    widget = widget.wrapper;
                    if (widget.hasAttribute('data-cke-widget-id') && widget.findOne('.page-file')) {
                        var target = widget.getParent();
                        if (target && !target.hasClass('page-files')) {
                            var wrapper = new CKEDITOR.dom.element('div', editor.document);
                            wrapper.addClass('page-files');
                            widget.insertBeforeMe(wrapper);
                            wrapper.append(widget);
                        }
                    }
                }, 20);
            });
        }
    })

})();
