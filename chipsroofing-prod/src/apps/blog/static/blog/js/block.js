(function($) {


    function ChangeSlider() {
        if ($(window).width() > 768){
            $(".container").removeClass('swiper-container');
            $(".container-wrapper").removeClass('swiper-wrapper');
            $(".container-slide").removeClass('swiper-slide');
        }
        else if ($(window).width() <= 768){
            $(".container").addClass('swiper-container');
            $(".container-wrapper").addClass('swiper-wrapper');
            $(".container-slide").addClass('swiper-slide');
        }
    }

    ChangeSlider();

    var mySwiper = undefined;
    function initSwiper() {
        var screenWidth = $(window).width();
        var $block = $('.news-block');

        if ( (screenWidth <= (768)) && (mySwiper == undefined)) {
            if ($block.length)
            {
                mySwiper = new Swiper($block.find('.swiper-container'), {
                    freeMode: false,
                    autoHeight: true,
                    threshold: 10,
                    slidesPerView: 2,

                    breakpoints: {
                        479: {
                            slidesPerView: 1,
                            spaceBetween: 20
                        },
                        769: {
                            slidesPerView: 2,
                            spaceBetween: 20
                        }
                    },

                    scrollbar: {
                        el: '.swiper-scrollbar'
                    }
                });
            }
        } else if ((screenWidth > 768) && (mySwiper != undefined)) {
            mySwiper.destroy();
            mySwiper = undefined;
        }
    }
    initSwiper();

    $(window).resize(function() {
        ChangeSlider();
        initSwiper();
    });

})(jQuery);