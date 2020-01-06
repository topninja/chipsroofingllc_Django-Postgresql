(function($) {

    /** @namespace window.js_storage.ajax_vote */

    var query;
    $(document).on('click', '.rating li', function() {
        var $star = $(this);

        var $list = $star.closest('.stars');
        if ($list.hasClass('voted')) {
            return false;
        }

        var rating = parseInt($star.data('vote')) || 5;
        if ((rating < 1) || (rating > 5)) {
            return false;
        }

        if (query) query.abort();
        query = $.ajax({
            url: window.js_storage.ajax_vote,
            type: 'POST',
            data: {
                rating: rating
            },
            dataType: 'json',
            success: function(response) {
                $list.attr('class', 'stars').addClass('voted voted-' + response.rating);
            }
        });
    }).ready(function() {
        var rating = $.cookie('voted');
        if (rating) {
            $('.rating').find('.stars').addClass('voted voted-' + rating);
        }
    });

})(jQuery);
