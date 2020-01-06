(function($) {

    /** @namespace window.js_storage.ajax_subscribe */

    /*
        Показ окна подписки
     */
    window.subscribePopup = function() {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_subscribe,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.form) {
                    var popup = $.popup({
                        classes: 'subscribe-popup subscribe-form-popup',
                        content: response.form
                    }).show();
                }
            },
            error: $.parseError(function() {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            })
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on('click', '.open-subscribe-popup', function() {
        subscribePopup();
        return false;
    });


    /*
        Отправка AJAX-формы подписки
     */
    $(document).on('submit', '#ajax-subscribe-form', function() {
        var $form = $(this);
        if ($form.hasClass('sending')) {
            return false;
        }

        $.ajax({
            url: window.js_storage.ajax_subscribe,
            type: 'post',
            data: $form.serialize(),
            dataType: 'json',
            beforeSend: function() {
                $form.addClass('sending');
                $form.find('.invalid').removeClass('invalid');
            },
            success: function(response) {
                if (response.success_message) {
                    // сообщение о успешной отправке
                    $.popup({
                        classes: 'subscribe-popup subscribe-success-popup',
                        content: response.success_message
                    }).show();

                    $form.get(0).reset();
                }
            },
            error: $.parseError(function(response) {
                if (response && response.errors) {
                    // ошибки формы
                    response.errors.forEach(function(record) {
                        var $field = $form.find('.' + record.fullname);
                        if ($field.length) {
                            $field.addClass(record.class);
                        }
                    });
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                    $.popup().hide();
                }
            }),
            complete: function() {
                $form.removeClass('sending');
            }
        });

        return false;
    });

})(jQuery);