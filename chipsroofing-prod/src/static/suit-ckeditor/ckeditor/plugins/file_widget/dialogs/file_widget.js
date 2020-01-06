(function() {

    /** @namespace editor.lang.file_widget */

    CKEDITOR.dialog.add('fileDialog', function(editor) {
        var lang = editor.lang.file_widget;
        return {
            title: lang.dialogTitle,
            minWidth: 320,
            minHeight: 100,
            resizable: false,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'name',
                    type: 'text',
                    required: true,
                    style: 'width:100%',
                    label: 'Name',
                    setup: function(widget) {
                        var text = widget.wrapper.findOne('span');
                        if (text) {
                            this.setValue(text.getText());
                            this.focus(true);
                        }
                    },
                    commit: function(widget) {
                        var text = widget.wrapper.findOne('span');
                        if (text) {
                            text.setText(this.getValue());
                        }
                    }
                }]
            }],
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
        };
    });

})();