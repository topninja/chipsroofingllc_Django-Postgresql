(function($) {

        $(document).ready(function() {
        var $block = $('.partners-block');
        if ($block.length) {
            var swiper = new Swiper($block.find('.swiper-container'), {
                autoHeight: true,
                slidesPerView: 8,
                spaceBetween: 40,
                freeMode: true,
                threshold: 20,
                breakpoints: {
                    479: {
                        slidesPerView: 3,
                        spaceBetween: 30
                    },
                    599: {
                        slidesPerView: 4,
                        spaceBetween: 30
                    },
                    799: {
                        slidesPerView: 5,
                        spaceBetween: 30
                    },
                    1023: {
                        slidesPerView: 6,
                        spaceBetween: 30
                    }
                },

                scrollbar: {
                    el: '.swiper-scrollbar'
                }
            });
        }
    });

})(jQuery);

