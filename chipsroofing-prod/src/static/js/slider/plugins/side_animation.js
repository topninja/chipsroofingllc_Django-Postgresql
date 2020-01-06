(function($) {
    'use strict';

    var DIRECTION_RIGHT = 'right';
    var DIRECTION_LEFT = 'left';

    window.SliderSideAnimation = Class(SliderAnimationPlugin, function SliderSideAnimation(cls, superclass) {
        cls.PLUGIN_NAME = 'side';

        cls.defaults = $.extend({}, superclass.defaults, {
            speed: 600,
            easing: 'easeOutCubic',
            animateListHeight: false,

            margin: 0,          // в пикселях или процентах
            showIntermediate: true
        });

        /*
            Построение настроек анимации.
            Учитывает опции, переданные через slider.slideTo()
         */
        cls.buildAnimationOptions = function(options) {
            return $.extend({
                speed: this.opts.speed,
                easing: this.opts.easing,
                animateListHeight: this.opts.animateListHeight,
                margin: this.opts.margin,
                showIntermediate: this.opts.showIntermediate
            }, options);
        };

        /*
            Выбор направления анимации
         */
        cls._chooseSlideDirection = function(slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;
            if (slide_info.toIndex > slide_info.fromIndex) {
                slide_info.count = diff;
                slide_info.direction = DIRECTION_RIGHT;
            } else {
                slide_info.count = -diff;
                slide_info.direction = DIRECTION_LEFT;
            }
        };

        /*
            Получение массива слайдов, которые нужно анимировать
         */
        cls._getAnimationSlides = function($currentSlide, $targetSlide, slide_info) {
            var slides = [];

            if (slide_info.direction === DIRECTION_RIGHT) {
                var doStepSlide = $.proxy(
                    this.slider.getNextSlide,
                    this.slider
                );
            } else {
                doStepSlide = $.proxy(
                    this.slider.getPreviousSlide,
                    this.slider
                );
            }

            // определяем слайды, учавствующие в анимации
            if (this.animationOptions.showIntermediate) {
                var i = 0;
                var $slide = $currentSlide;
                while ($slide.length && (i++ <= slide_info.count)) {
                    slides.push($slide);
                    $slide = doStepSlide($slide);
                }
            } else {
                slides.push($currentSlide);
                slides.push($targetSlide);
            }

            return slides;
        };

        /*
            Перевод отступа в пикселях в отступ в процентах
         */
        cls._getPercentGap = function() {
            if (this.animationOptions.margin.toString().indexOf('%') >= 0) {
                return parseFloat(this.animationOptions.margin);
            } else {
                var slider_width = this.slider.$list.outerWidth();
                return 100 * parseFloat(this.animationOptions.margin) / slider_width;
            }
        };

        /*
            Создание объектов для анимирования
         */
        cls._makeAnimations = function(slides, slide_info) {
            var animations = [];
            var count = slides.length;
            var slide_width = 100;  // в процентах
            var slide_gap = this._getPercentGap();
            var direction_multiplier = slide_info.direction === DIRECTION_RIGHT ? 1 : -1;

            $.each(slides, function(index, $slide) {
                var left = index * (slide_width + slide_gap) * direction_multiplier;
                $slide.css({
                    transform: 'translate(' + left + '%, 0%)'
                });
                animations.push({
                    $slide: $slide,
                    start: left,
                    end: (count - index - 1) * (slide_width + slide_gap) * -direction_multiplier
                });
            });

            return animations;
        };

        /*
            Подготовка слайдов к анимации
         */
        cls.prepareAnimation = function($currentSlide, $targetSlide) {
            superclass.prepareAnimation.call(this, $currentSlide, $targetSlide);

            var slide_info = {
                fromIndex: this.slider.$slides.index($currentSlide),
                toIndex: this.slider.$slides.index($targetSlide)
            };

            // выбор направления анимации
            this._chooseSlideDirection(slide_info);

            // получение массива слайдов, которые нужно анимировать
            var slides = this._getAnimationSlides($currentSlide, $targetSlide, slide_info);

            // cоздание объекта, описывающего анимацию слайдов
            this.animations = this._makeAnimations(slides, slide_info);

            // добавляем overflow, чтобы не было видно соседних слайдов
            this.slider.$list.css({
                overflow: 'hidden'
            });
        };

        /*
            Запуск анимации
         */
        cls.startAnimation = function($currentSlide, $targetSlide) {
            superclass.startAnimation.call(this, $currentSlide, $targetSlide);

            var state_from = {};
            var state_to = {};
            $.each(this.animations, function(index, data) {
                state_from[index] = data.start;
                state_to[index] = data.end;
            });

            var that = this;
            this.slider._animation = $(state_from).animate(state_to, {
                duration: this.animationOptions.speed,
                easing: this.animationOptions.easing,
                progress: function() {
                    var state = this;
                    $.each(that.animations, function(index, data) {
                        data.$slide.css({
                            transform: 'translate(' + state[index] + '%, 0%)'
                        })
                    });
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
            // сбрасываем стили всех, кроме последнего слайда
            for (var i=0; i<(this.animations.length - 1); i++) {
                this.animations[i].$slide.css({
                    transform: ''
                })
            }

            this.slider.$list.css({
                overflow: ''
            });

            superclass.endAnimation.call(this, $currentSlide, $targetSlide);
        };
    });


    //========================================================
    //  Анимация, выбирающая направление, соответствующее
    //  кратчайшему пути.
    //========================================================
    window.SliderSideShortestAnimation = Class(SliderSideAnimation, function SliderSideShortestAnimation(cls, superclass) {
        cls.PLUGIN_NAME = 'side-shortest';

        /*
            Выбор направления анимации
         */
        cls._chooseSlideDirection = function(slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;
            if (this.slider.opts.loop) {
                var slides_count = this.slider.$slides.length;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (left_way < right_way) {
                    slide_info.count = left_way;
                    slide_info.direction = DIRECTION_LEFT;
                } else {
                    slide_info.count = right_way;
                    slide_info.direction = DIRECTION_RIGHT;
                }
            } else {
                if (slide_info.toIndex > slide_info.fromIndex) {
                    slide_info.count = diff;
                    slide_info.direction = DIRECTION_RIGHT;
                } else {
                    slide_info.count = -diff;
                    slide_info.direction = DIRECTION_LEFT;
                }
            }
        };
    });

})(jQuery);
