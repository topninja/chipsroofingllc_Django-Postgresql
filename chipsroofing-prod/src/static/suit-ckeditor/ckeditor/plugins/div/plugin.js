(function() {
    var WIDGET_NAME = 'div';

    CKEDITOR.plugins.add("div", {
        requires: 'widget',
        icons: 'div',
        init: function (editor) {
            editor.addContentsCss(this.path + 'styles/widget.css');

            // ======================================
            //      Dialogs
            // ======================================

            CKEDITOR.dialog.add("divDialog", this.path + "dialogs/div.js");

            // ======================================
            //      Widgets
            // ======================================
            editor.widgets.add(WIDGET_NAME, {
                button: 'Add Div Container',
                dialog: 'divDialog',
                allowedContent: 'div[data-widget-name](*)',
                requiredContent: 'div[data-widget-name](*)',
                template: '<div data-widget-name="div"></div>',
                editables: {
                    root: {
                        selector: 'div[data-widget-name="div"]'
                    }
                },
                init: function() {
                    var activeStyle = CKEDITOR.utils.getActiveStyle(editor, this.element);
                    if (activeStyle) {
                        this.setData('styleName', activeStyle.name);
                    }
                },
                data: function() {
                    var widget = this;
                    if (widget.data.styleName) {
                        editor.getStylesSet(function(styleSet) {
                            if (!styleSet) return;
                            for (var i=0; i<styleSet.length; i++) {
                                var style = styleSet[i];
                                if (style.name === widget.data.styleName) {
                                    var styleObj = new CKEDITOR.style(style);
                                    styleObj.applyToObject(widget.element);
                                    return false;
                                }
                            }
                        });
                    } else {
                        // удаление классов, не начинающихся на "cke_"
                        widget.element.$.className = Array.prototype.slice.apply(
                            widget.element.$.classList
                        ).filter(function(name) {
                            return name.substr(0, 4) === 'cke_';
                        }).join(' ');
                    }
                },
                upcast: function(element) {
                    return element.name === 'div' && (element.attributes['data-widget-name'] === WIDGET_NAME);
                }
            });

            // ======================================
            //      Commands
            // ======================================
            editor.addCommand("edit_div", new CKEDITOR.dialogCommand("divDialog"));

            // ======================================
            //      Context Menu
            // ======================================
            if (editor.contextMenu) {
                editor.addMenuGroup('divGroup');
                editor.addMenuItem('divItem', {
                    label: 'Edit Div',
                    icon: this.path + 'icons/edit.png',
                    command: 'edit_div',
                    group: 'divGroup'
                });

                editor.contextMenu.addListener(function(element) {
                    var widget = editor.widgets.getByElement(element);
                    if (widget && widget.name === WIDGET_NAME) {
                        return {
                            divItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                });
            }

            editor.widgets.on('instanceCreated', function(evt) {
                var widget = evt.data;
                widget.on('key', function(event) {
                    if ((event.data.keyCode === 13) && (event.sender.name === WIDGET_NAME)) {
                        var p = editor.document.createElement('p');
                        p.setHtml('&nbsp;');
                        p.insertAfter(this.wrapper);

                        var selection = editor.getSelection();
                        var range = selection.getRanges()[0];
                        var newRange = new CKEDITOR.dom.range(range.document);
                        newRange.moveToPosition(p, CKEDITOR.POSITION_BEFORE_START);
                        newRange.select();
                        selection.scrollIntoView();
                        return false;
                    }
                });
            });
        }
    });

})();
