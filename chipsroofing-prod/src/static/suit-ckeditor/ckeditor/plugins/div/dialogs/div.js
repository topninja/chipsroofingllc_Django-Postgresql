(function() {

    CKEDITOR.dialog.add("divDialog", function(editor) {
        var styles = {};
        return {
            title: 'Create Div Container',
            minWidth: 200,
            minHeight: 100,
            contents: [{
                id: 'info',
                elements: [
                    {
                        id: 'elementStyle',
                        type: 'select',
                        style: 'width: 200px;',
                        label: 'Style',
                        items: [
                            [editor.lang.common.notSet, '']
                        ],
                        onChange: function() {
                            var dialog = this.getDialog();
                            var widget = dialog._widget;
                            if (widget) {
                                this.commit(widget, true);
                            }
                        },
                        setup: function(widget) {
                            /** @namespace widget.data.styleName */
                            var style = widget.data.styleName;
                            if (style) {
                                this.setValue(style);
                            }
                        },
                        commit: function(widget) {
                            widget.setData('styleName', this.getValue());
                        }
                    }
                ]
            }],
            onLoad: function() {
                var dialog = this;
                var stylesField = this.getContentElement('info', 'elementStyle');

                // load all Available styles
                var allowedStyles = CKEDITOR.utils.getAllowedStyles(editor, 'div');
                allowedStyles.forEach(function(item) {
                    var styleName = item.name;
                    var style = new CKEDITOR.style(item);
                    styles[styleName] = style;
                    if (editor.filter.check(style)) {
                        stylesField.items.push([styleName, styleName]);
                        stylesField.add(styleName, styleName);
                    }
                });

                if (stylesField.items.length > 1) {
                    stylesField.enable();
                } else {
                    stylesField.disable();
                }

                setTimeout(function() {
                    dialog._widget && stylesField.setup(dialog._widget);
                }, 0);
            },
            onShow: function() {
                var element = editor.getSelection().getStartElement();
                var widget = editor.widgets.getByElement(element);
                if (widget) {
                    this.setupContent(this._widget = widget);
                }
            },
            onOk: function() {
                if (this._widget) {
                    this.commitContent(this._widget);
                }
            }
        }
    })

})();
