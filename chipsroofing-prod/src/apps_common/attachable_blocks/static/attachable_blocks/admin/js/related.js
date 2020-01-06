(function($) {

    var REF_PREFIX = 'attachable_blocks-attachablereference';
    var DATA_ATTR = 'data-href-block-template';

    var ADD_URL_TEMPLATE = '/dladmin/ctr/add/__ct__/?_to_field=id&_popup=1';
    var CHANGE_URL_TEMPLATE = '/dladmin/ctr/change/__ct__/__pk__/?_to_field=id&_popup=1';
    var DELETE_URL_TEMPLATE = '/dladmin/ctr/delete/__ct__/__pk__/?_to_field=id&_popup=1';

    /*
        Создание DOM-элемента кнопки добавления
     */
    var generate_add_button =function($field) {
        var $link = $('<a>').addClass('related-widget-wrapper-link add-related');
        $link.attr('id', 'add_id_' + $field.attr('name'));
        $link.attr('title', gettext('Add another'));
        $link.attr(DATA_ATTR, ADD_URL_TEMPLATE);
        return $link;
    };

    /*
        Создание DOM-элемента кнопки редактирования
     */
    var generate_change_button = function($field) {
        var $link = $('<a>').addClass('related-widget-wrapper-link change-related');
        $link.attr('id', 'change_id_' + $field.attr('name'));
        $link.attr('title', gettext('Edit'));
        $link.attr(DATA_ATTR, CHANGE_URL_TEMPLATE);
        return $link;
    };

    /*
        Создание DOM-элемента кнопки удаления
     */
    var generate_delete_button = function($field) {
        var $link = $('<a>').addClass('related-widget-wrapper-link delete-related');
        $link.attr('id', 'change_id_' + $field.attr('name'));
        $link.attr('title', gettext('Delete'));
        $link.attr(DATA_ATTR, DELETE_URL_TEMPLATE);
        return $link;
    };

    /*
        Обновление ссылки на кнопке добавления
     */
    var update_add_button = function($button, content_type) {
        if ($button.length !== 1) {
            console.warn('more than one related button');
            return
        }

        if (!content_type) {
            $button.removeAttr('href');
            return
        }

        var href = $button.attr(DATA_ATTR);
        href = href.replace('__ct__', content_type);
        $button.attr('href', href);
    };

    /*
        Обновление ссылки на кнопке редактирования и удаления
     */
    var update_change_button = function($button, content_type, pk) {
        if ($button.length !== 1) {
            console.warn('more than one related button');
            return
        }

        if (!content_type || !pk) {
            $button.removeAttr('href');
            return
        }

        var href = $button.attr(DATA_ATTR);
        href = href.replace('__ct__', content_type);
        href = href.replace('__pk__', pk || '');
        $button.attr('href', href);
    };

    /*
        Обновление ссылок на всех кнопках
     */
    var update_buttons = function(object) {
        var block_id = object.$elem.val();
        var $content_type_field = object.$filters;
        var content_type = $content_type_field.val();
        if (content_type) {
            update_add_button(object.$elem.siblings('.add-related'), content_type);
            if (block_id) {
                update_change_button(object.$elem.siblings('.change-related'), content_type, block_id);
                update_change_button(object.$elem.siblings('.delete-related'), content_type, block_id);
            }
        }
    };

    /*
        Инициализация кнопок автокомплит-поля
     */
    var init_field = function($field) {
        // TODO: хак для суперюзера
        if (!window.is_superuser) {
            return
        }

        var obj = $field.data(Autocomplete.prototype.DATA_KEY);
        if (!obj || (obj.$filters.length !== 1)) {
            return
        }

        // кнопка удаления
        var $delete_button = generate_delete_button($field);
        $field.after($delete_button);

        // кнопка редактирования
        var $change_button = generate_change_button($field);
        $field.after($change_button);

        // кнопка добавления
        var $add_button = generate_add_button($field);
        $field.after($add_button);


        // обновление при изменении типа блока
        var $content_type_field = obj.$filters.first();
        $content_type_field.on('change', function() {
            update_buttons(obj);
        });

        // обновление при изменении блока
        $field.on('change', function() {
            update_buttons(obj);
        });

        update_buttons(obj);
    };

    $(document).ready(function() {
        // формсеты инлайнов с подключаемыми блоками
        var $formsets = $('.inline-group[id^="' + REF_PREFIX + '"]');
        $formsets.find('input.autocomplete_widget').each(function() {
            init_field($(this));
        });

        if (window.Suit) {
            Suit.after_inline.register('attachable_blocks_buttons', function(inline_prefix, row) {
                row.find('.autocomplete_widget').each(function() {
                    init_field($(this));
                });
            });
        }
    });

})(jQuery);