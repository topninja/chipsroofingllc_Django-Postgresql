(function($) {

    $(document).on('click', '#show_more', function() {
        var preloader = $.preloader(),
            page = $(this).data('page'),
            perpage = $(this).data('perpage');

        $.ajax({
            url: window.js_storage.ajax_blog,
            type: 'GET',
            data: {
                'page': page,
                'perpage': perpage
            },
            dataType: 'json',
            success: function(response) {
                if (response.success_message) {
                    $('#show_more').remove();

                    var $response = $(response.success_message),
                        $items_wrapper = $('#posts'),
                        $showmore = null,
                        $items;

                    if ($response.last().attr('id') === 'show_more'){
                        $showmore = $response.last();
                        $items = $response.slice(0, -1);
                    }else{
                        $items = $response;
                    }

                    $items_wrapper.append($items);
                    $items = $('.post');

                    if ($showmore){$showmore.insertAfter($items_wrapper)}
                    $.scrollTo($items.last(), 800);
                }
                preloader.destroy();
            },
            error: $.parseError(function() {
                preloader.destroy();
                alert(window.DEFAULT_AJAX_ERROR);
            })
        });
        return false;
    });


    $(document).ready(function() {

    });

})(jQuery);