(function ($) {

    /** @namespace window.js_storage.ajax_contact */
    /** @namespace window.js_storage.ajax_free_estimate */

    /*
        Показ окна контактов
     */
    window.contactPopup = function () {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                if (response.form) {
                    var popup = $.popup({
                        classes: 'contact-popup contact-form-popup',
                        content: response.form
                    }).show();

                    window.initPopRecaptcha();

                }
            },
            error: $.parseError(function () {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            })
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on('click', '.open-contact-popup', function () {
        contactPopup();
        return false;
    });

    $(document).on('click', '#ajax-contact-submit', function (e) {
        e.preventDefault();

        var token = window.grecaptcha.getResponse(popup_recaptchaId);

        if (!token) {
            window.grecaptcha.execute(popup_recaptchaId);
            return;
        }
    });


    /*
        Отправка AJAX-формы со страницы
     */


    /*
        Отправка AJAX-формы из попапа
     */
    window.popupSend = function (token) {
        var $form = $('#ajax-popup-contact-form');
        if ($form.hasClass('sending')) {
            return false;
        }

        // добавление адреса страницы, откуда отправлена форма
        var data = $form.serializeArray();
        data.push({
            name: 'referer',
            value: location.href
        });
        data.push({
            name: 'g-recaptcha-response',
            value: token
        });

        $.ajax({
            url: window.js_storage.ajax_contact,
            type: 'post',
            data: data,
            dataType: 'json',
            beforeSend: function () {
                // $.popup.showPreloader();
                $form.addClass('sending');
                $form.find('.invalid').removeClass('invalid');
            },
            success: function (response) {
                $.popup({
                        classes: 'contact-popup contact-success-popup',
                        content: response.success_message
                    }).show();
                $.popup.hidePreloader();
                $form.get(0).reset()

            },
            error: $.parseError(function (response) {
                // $.popup.hidePreloader();

                if (response && (response.errors || response.recaptcha_is_valid == 'false')) {
                    // ошибки формы
                    response.errors.forEach(function (record) {
                        var $field = $form.find('.' + record.fullname);
                        if ($field.length) {
                            $field.addClass(record.class);
                        }
                    });

                    if (response.recaptcha_is_valid == false) {
                        $form.find('.g-recaptcha').addClass('invalid');
                    } else {
                        window.grecaptcha.reset(popup_recaptchaId);
                    }
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                }
            }),
            complete: function () {
                $form.removeClass('sending');
            }
        });

        return false;
    };

    window.EstimatePopup = function () {
        $.preloader();

        return $.ajax({
            url: window.js_storage.ajax_free_estimate,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                if (response.form) {
                    var popup = $.popup({
                        classes: 'contact-popup contact-form-popup',
                        content: response.form
                    }).show();

                    window.initPopRecaptcha();

                }
            },
            error: $.parseError(function () {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            })
        });
    };


    /*
        Открытие окна контактов при клике на кнопки
     */
    $(document).on('click', '.open-free-estimate-popup', function () {
        EstimatePopup();
        return false;
    });

    $(document).on('click', '#ajax-estimate-submit', function (e) {
        e.preventDefault();

        var token = window.grecaptcha.getResponse(popup_recaptchaId);

        if (!token) {
            window.grecaptcha.execute(popup_recaptchaId);
            return;
        }
    });


    /*
        Отправка AJAX-формы из попапа
     */
    window.popupSendEstimate = function (token) {
        var $form = $('#ajax-free-estimate-form');
        if ($form.hasClass('sending')) {
            return false;
        }

        // добавление адреса страницы, откуда отправлена форма
        var data = $form.serializeArray();
        data.push({
            name: 'referer',
            value: location.href
        });
        data.push({
            name: 'g-recaptcha-response',
            value: token
        });

        $.ajax({
            url: window.js_storage.ajax_free_estimate,
            type: 'post',
            data: data,
            dataType: 'json',
            beforeSend: function () {
                // $.popup.showPreloader();
                $form.addClass('sending');
                $form.find('.invalid').removeClass('invalid');
            },
            success: function (response) {
                $.popup({
                        classes: 'contact-popup contact-success-popup',
                        content: response.success_message
                    }).show();
                $.popup.hidePreloader();
                $form.get(0).reset()

            },
            error: $.parseError(function (response) {
                // $.popup.hidePreloader();

                if (response && (response.errors || response.recaptcha_is_valid == 'false')) {
                    // ошибки формы
                    response.errors.forEach(function (record) {
                        var $field = $form.find('.' + record.fullname);
                        if ($field.length) {
                            $field.addClass(record.class);
                        }
                    });

                    if (response.recaptcha_is_valid == false) {
                        $form.find('.g-recaptcha').addClass('invalid');
                    } else {
                        window.grecaptcha.reset(popup_recaptchaId);
                    }
                } else {
                    alert(window.DEFAULT_AJAX_ERROR);
                }
            }),
            complete: function () {
                $form.removeClass('sending');
            }
        });

        return false;
    };

    var popup_recaptchaId;
    window.initPopRecaptcha = function () {
        var recaptchaElement = document.querySelector('#popup_recaptcha');
        var recaptchaElementEstimate = document.querySelector('#popup_recaptcha_estimate');

        var captchaOptions = {
            sitekey: $(recaptchaElement).data('sitekey'),
            size: 'invisible',
            callback: window.popupSend
        };
        var captchaOptionsEstimate = {
            sitekey: $(recaptchaElementEstimate).data('sitekey'),
            size: 'invisible',
            callback: window.popupSendEstimate
        };

        var inheritFromDataAttr = true;

        if ($('#popup_recaptcha').length) {
            popup_recaptchaId = window.grecaptcha.render(recaptchaElement, captchaOptions, inheritFromDataAttr);
        }
        if ($('#popup_recaptcha_estimate').length) {
            popup_recaptchaId = window.grecaptcha.render(recaptchaElementEstimate, captchaOptionsEstimate, inheritFromDataAttr);
        }

    };


})(jQuery);