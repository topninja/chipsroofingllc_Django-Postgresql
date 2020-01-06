(function() {

    /** @namespace CKEDITOR.dialog */
    /** @namespace editor.lang.pagephotos */

    var clean_element = function(element) {
        var i = 0;
        var child;
        var childs = element.childNodes;
        while (child = childs[i]) {
            if (child.nodeType !== 1) {
                element.removeChild(child);
            } else if (child.tagName !== 'IMG') {
                element.removeChild(child);
            } else {
                i++
            }
        }
    };

    CKEDITOR.dialog.add("pagephotos_block_description", function (editor) {
        var lang = editor.lang.pagephotos;
        return {
            title: lang.dialogBlockDescr,
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'description',
                    type: 'textarea',
                    label: lang.dialogBlockDescrTextarea
                }]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();
                var container = element.hasClass('page-images') ? element : element.getParent();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                var description = CKEDITOR.tools.trim(container.$.innerText);
                textarea.setValue( description );
                textarea.focus(true);
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();
                var container = element.hasClass('page-images') ? element : element.getParent();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                clean_element(container.$);

                var description = CKEDITOR.tools.trim(textarea.getValue());
                if (description) {
                    description = description.replace(/\n/g, '<br/>');
                    container.appendHtml('<br/> ' + description);
                }
            }
        }
    })

})();
