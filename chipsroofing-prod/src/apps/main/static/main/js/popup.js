(function ($) {

    window.servicePopup = function (service) {
        $.preloader();
        return $.ajax({
            url: window.js_storage.ajax_main,
            data: {'param': service},
            type: 'POST',
            dataType: 'json',
            success: function (response) {
                var popup = $.popup({
                    content: response.service_popup
                }).show();
                $('#popup-container').addClass('service-popup')
            },
            error: $.parseError(function () {
                alert(window.DEFAULT_AJAX_ERROR);
                $.popup().hide();
            })
        });
    };

    $(document).on('click', '.siding', function () {
        servicePopup(service = 'siding');
        return service;
    });

    $(document).on('click', '.gutters', function () {
        servicePopup(service = 'gutters');
        return service;
    });

    $(document).on('click', '.new-roofing', function () {
        servicePopup(service = 'new-roofing');
        return service;
    });

    $(document).on('click', '.commercial-roofing', function () {
        servicePopup(service = 'commercial-roofing');
        return service;
    });

    $(document).on('click', '.residential-roofing', function () {
        servicePopup(service = 'residential-roofing');
        return service;
    });

    $(document).on('click', '.roof-repairs', function () {
        servicePopup(service = 'roof-repairs');
        return service;
    });

})(jQuery);
