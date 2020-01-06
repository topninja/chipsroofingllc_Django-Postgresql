(function($) {

    /** @namespace window.js_storage.fb_banner_url */
    /** @namespace window.js_storage.fb_banner_timeout */

    window.fbAsyncInit = function() {
        $(document).trigger('init.fb')
    };

    $(document).on('click', '#facebook-banner .close-button', function() {
        $('#facebook-banner').fadeOut(300, function() {
            $(this).remove()
        });
        $.cookie('fb-banner-shown', 1, {
            expires: 30,
            path: '/'
        });
    }).on('init.fb', function() {
        if ($.cookie('fb-banner-shown')) {
            return
        }

        if ($.winWidth() < 640) {
            return
        }

        $.ajax({
            url: window.js_storage.fb_banner_url,
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.html) {
                    $('#facebook-banner').remove();
                    $(document.body).append(response.html);
                }

                setTimeout(function() {
                    $('#facebook-banner').fadeIn(300);
                }, window.js_storage.fb_banner_timeout);
            }
        });
    });

})(jQuery);