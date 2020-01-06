
'use strict';

( function() {
    CKEDITOR.plugins.add( 'textlen', {
        init: function( editor ) {
            // This feature is available only for themed ui instance.
            if ( editor.elementMode === CKEDITOR.ELEMENT_MODE_INLINE )
                return;

            var get_clear_textlen = function(text) {
                var trimmed = $.trim(text.replace(/<\/?[^>]+>/gi, '').replace(/(&nbsp;|&laquo;|&raquo)/g, " ").replace(/ +/g, " "));
                return trimmed.length;
            };

            editor.on('instanceReady', function(){
                var element = this.document.createElement('span'),
                    current_html = this.document.getBody().getHtml(),
                    bottom = this.ui.space('bottom');

                element.setAttribute('title', 'Длина введенного текста');
                element.addClass('cke_path_item');
                element.setStyles({
                    margin: '-2px 0 2px',
                    border: '1px solid #6c6c6c'
                });
                element.setText(get_clear_textlen(current_html));
                bottom.append(element, true);

                $(this.document.$).on('keyup', function() {
                    var current_html = this.body.innerHTML.replace(/<\/p>([^$]+?)/g, '</p>\n$1');
                    bottom.$.getElementsByClassName('cke_path_item').item(0).textContent = get_clear_textlen(current_html);
                });
            });
        }
    } );

} )();
