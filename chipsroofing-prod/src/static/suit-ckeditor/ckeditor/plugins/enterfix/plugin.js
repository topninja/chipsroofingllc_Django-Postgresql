/*
Запрещаем копировать классы и атрибуты при нажатии Enter
*/
(function() {

    CKEDITOR.plugins.add( 'enterfix', {
        init: function(editor) {
            editor.on('key', function(evt) {
                if (editor.mode !== "wysiwyg") {
                    return
                }

                if (evt.data.keyCode === 13) {
                    // if we call getStartElement too soon, we get the wrong element
                    setTimeout(function() {
                        var se = editor.getSelection().getStartElement();
                        se.removeAttribute("class");
                        se.removeAttribute("style");
                    }, 10);
                }
            });
        }
    } );

})();
