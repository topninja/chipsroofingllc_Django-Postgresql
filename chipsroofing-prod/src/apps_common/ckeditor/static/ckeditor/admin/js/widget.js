(function($) {

    /** @namespace window._ckeditor_confs */

    $(document).ready(function() {
        var configs = window._ckeditor_confs;
        if (!configs) return;

        for (var name in configs) {
            if (!configs.hasOwnProperty(name)) continue;

            // ищем поле
            var $field = $('.ckeditor-field[name="' + name + '"]');
            if ($field.length !== 1) continue;

            // шаблонная inline-форма
            if ($field.closest('.empty-form').length) continue;

            // получаем настройки и инициализируем CKEditor
            var config = configs[name];
            CKEDITOR.replace(name, config);
        }

        if (window.Suit) {
            Suit.after_inline.register('ckeditor-field', function(inline_prefix, row) {
                row.find('.ckeditor-field').each(function() {
                    var $field = $(this);
                    var name = $field.attr('name');
                    var name_arr = name.split('-');
                    var template_name = name_arr.slice(0, -2).concat(
                        '__prefix__', name_arr[name_arr.length - 1]
                    ).join('-');
                    var config = window._ckeditor_confs[template_name];

                    CKEDITOR.replace(name, config);
                });
            });
        }
    });

})(jQuery);