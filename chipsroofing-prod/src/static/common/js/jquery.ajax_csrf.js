(function($) {

    // Устанавливаем CSRF-токен всем AJAX-запросам
    $(document).ajaxSend(function(event, xhr, settings) {
        if (!/^https?:\/\//i.test(settings.url)) {
            var csrf = $('input[name=csrfmiddlewaretoken]:eq(0)').val();
            if (!csrf) {
                csrf = $.cookie('csrftoken')
            }

            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    });

})(jQuery);
