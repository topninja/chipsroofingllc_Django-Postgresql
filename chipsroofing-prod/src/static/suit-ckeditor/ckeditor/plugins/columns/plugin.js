(function() {
    var WIDGET_NAME = 'columns';

    CKEDITOR.plugins.add("columns", {
        requires: 'widget',
        icons: 'columns',
        init: function (editor) {
            editor.addContentsCss(this.path + 'styles/widget.css');

            // ======================================
            //      Widgets
            // ======================================
            editor.widgets.add(WIDGET_NAME, {
                button: 'Two columns',
                allowedContent: 'div',
                requiredContent: 'div(columns)',
                template: '<div class="columns">' +
                              '<div class="column column-left"></div>' +
                              '<div class="column column-right"></div>' +
                          '</div>',
                editables: {
                    left: {
                        selector: '.column-left'
                    },
                    right: {
                        selector: '.column-right'
                    }
                },
                upcast: function(element) {
                    return element.name === 'div' && element.hasClass('columns');
                }
            });

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
                        return false
                    }
                });
            });
        }
    })

})();
