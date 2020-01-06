(function($) {

    $(document).ready(function() {

        var wrap = $('.wrap-testimonial');

        if (wrap.find('.testimonial').length) {

            var rat = wrap.find('.contain-star');
            for (var i = 0; i < rat.length; i++) {
                var num = rat.eq(i).attr('data-star');
                var rest = 5 - num;
                for (var j = 0; j < num; j++) {
                    rat.eq(i).append('<div class="star-active"></div>');
                }
                for (var k = 0; k < rest; k++) {
                    rat.eq(i).append('<div class="star-off"></div>');
                }
            }
        }
    });

})(jQuery);