(function($) {
    'use strict';

    window.SliderFadeAnimation = Class(SliderAnimationPlugin, function SliderFadeAnimation(cls, superclass) {
        cls.PLUGIN_NAME = 'fade';

        cls.defaults = $.extend({}, superclass.defaults, {
            speed: 800,
            easing: 'linear',
            animateListHeight: false
        });

        /*
            Построение настроек анимации.
            Учитывает опции, переданные через slider.slideTo()
         */
        cls.buildAnimationOptions = function(options) {
            return $.extend({
                speed: this.opts.speed,
                easing: this.opts.easing,
                animateListHeight: this.opts.animateListHeight
            }, options);
        };

        /*
            Подготовка слайдов к анимации
         */
        cls.prepareAnimation = function($currentSlide, $targetSlide) {
            superclass.prepareAnimation.call(this, $currentSlide, $targetSlide);

            $currentSlide.css({
                zIndex: 6
            });
            $targetSlide.css({
                transform: 'none',
                opacity: 0,
                zIndex: 7
            });
        };

        /*
            Запуск анимации
         */
        cls.startAnimation = function($currentSlide, $targetSlide) {
            superclass.startAnimation.call(this, $currentSlide, $targetSlide);

            var that = this;
            this.slider._animation = $({
                progress: 0
            }).animate({
                progress: 1
            }, {
                duration: this.animationOptions.speed,
                easing: this.animationOptions.easing,
                progress: function () {
                    $currentSlide.css('opacity', (1 - this.progress));
                    $targetSlide.css('opacity', this.progress);
                },
                complete: function() {
                    that.endAnimation($currentSlide, $targetSlide);
                }
            });
        };

        /*
            Callback завершения анимации
         */
        cls.endAnimation = function($currentSlide, $targetSlide) {
            $currentSlide.css({
                transform: '',
                zIndex: '',
                opacity: ''
            });

            $targetSlide.css({
                zIndex: '',
                opacity: ''
            });

            superclass.endAnimation.call(this, $currentSlide, $targetSlide);
        };
    });

})(jQuery);
