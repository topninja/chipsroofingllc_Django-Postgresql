(function($) {
    'use strict';

    window.SliderDragPlugin = Class(SliderPlugin, function SliderDragPlugin(cls, superclass) {
        cls.PLUGIN_NAME = 'drag';

        cls.defaults = $.extend({}, superclass.defaults, {
            animateListHeight: true,

            mouse: true,
            touch: true,
            ignoreDistanceX: 16,
            ignoreDistanceY: 16,

            // На сколько процентов нужно перетащить слайд, чтобы изменился текущий слайд
            threshold: 10,

            // Расстояние между слайдами
            margin: 0,

            // Разрешено ли тащить граничные слайды (при loop = false)
            dragBounds: true,

            speed: 800,
            container: null,
            easing: 'easeOutCubic'
        });

        /*
            Включение плагина
         */
        cls.enable = function() {
            this.drager.attach();
            superclass.enable.call(this);
        };

        /*
            Выключение плагина
         */
        cls.disable = function() {
            this.drager.detach();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            if (this.drager) {
                this.drager.destroy();
                this.drager = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание объекта Drager
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this._attachEvents();
            this.checkUnselectable();
            this._updateEnabledState();
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.onUpdateSlides = function() {
            this.checkUnselectable();
            this._updateEnabledState();
        };

        /*
            Навешивание событий
         */
        cls._attachEvents = function() {
            var that = this;
            this.drager = Drager(this.getContainer(), {
                mouse: this.opts.mouse,
                touch: this.opts.touch,
                ignoreDistanceX: this.opts.ignoreDistanceX,
                ignoreDistanceY: this.opts.ignoreDistanceY,
                momentum: false
            }).on('dragstart', function(evt) {
                // если один слайд - выходим
                if (that.slider.$slides.length < 2) {
                    this.setStartPoint(evt);
                    return false;
                }

                // если идет анимация - прекращаем её
                that.slider.stopAnimation(true);

                // добавляем overflow, чтобы не было видно соседних слайдов
                that.slider.$list.css({
                    overflow: 'hidden'
                });

                that.onStartDrag(evt);
            }).on('drag', function(evt) {
                if (evt.abs_dx > evt.abs_dy) {
                    // по X движение больше
                    that.onDrag(evt);
                    return false
                }
            }).on('dragend', function(evt) {
                that.onStopDrag(evt);
            });
        };

        /*
            Получение контейнера для элементов
         */
        cls.getContainer = function() {
            if (typeof this.opts.container === 'string') {
                var $container = this.slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                $container = this.opts.container.call(this);
            } else if (this.opts.container && this.opts.container.jquery) {
                $container = this.opts.container;
            }

            if (!$container || !$container.length) {
                $container = this.slider.$listWrapper;
            } else if ($container.length) {
                $container = $container.first();
            }

            return $container;
        };

        /*
            Проверка, нужно ли блокировать выделение текста
         */
        cls.checkUnselectable = function() {
            if (this.slider.$slides.length >= 2) {
                this.slider.$root.addClass('unselectable');
            } else {
                this.slider.$root.removeClass('unselectable');
            }
        };

        /*
            Перевод смещения в пикселях в смещение в процентах от ширины слайдера
         */
        cls._dxToPercents = function(evt) {
            return 100 * evt.dx / this._sliderWidth;
        };

        /*
            Перевод отступа в пикселях в отступ в процентах от ширины слайдера
         */
        cls._getPercentGap = function() {
            if (this.opts.margin.toString().indexOf('%') >= 0) {
                return parseFloat(this.opts.margin);
            } else {
                return 100 * parseFloat(this.opts.margin) / this._sliderWidth;
            }
        };

        /*
            Начало перетаскивания слайдов мышью или тачпадом
         */
        cls.onStartDrag = function() {
            this._slides = [];
            this._transforms = [];
            this._$startSlide = this.slider.$currentSlide;
            this._sliderWidth = this.slider.$list.outerWidth();

            this.slider.trigger('startDrag');
            this.slider.callPluginsMethod('startDrag');
        };

        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        cls.onDrag = function(evt) {
            var dragLeft = evt.dx < 0;
            var dxPercents = this._dxToPercents(evt);
            var absDxPercents = Math.abs(dxPercents);
            var slidesDistance = 100 + this._getPercentGap();

            // очищаем позицию слайдов, которые перемещались ранее
            $(this._slides.filter(Boolean)).css({
                transform: ''
            });

            // находим центральный слайд
            var slideOffset = absDxPercents;
            var $centerSlide = this._$startSlide;
            if (dragLeft) {
                while (slideOffset > slidesDistance) {
                    var $slide = this.slider.getNextSlide($centerSlide);
                    if (!$slide.length) {
                        break;
                    }

                    $centerSlide = $slide;
                    slideOffset -= slidesDistance;
                }
            } else {
                while (slideOffset > slidesDistance) {
                    $slide = this.slider.getPreviousSlide($centerSlide);
                    if (!$slide.length) {
                        break;
                    }

                    $centerSlide = $slide;
                    slideOffset -= slidesDistance;
                }
            }

            // нормализация
            slideOffset = Math.min(slideOffset, 100);

            // находим соседние слайды
            var $leftSlide = this.slider.getPreviousSlide($centerSlide);
            var $rightSlide = this.slider.getNextSlide($centerSlide);


            // =============================
            //  Определяем активный слайд
            // =============================
            var $currentSlide = $centerSlide;
            if (slideOffset > this.opts.threshold) {
                if (dragLeft) {
                    $currentSlide = $rightSlide;
                } else {
                    $currentSlide = $leftSlide;
                }
            }

            if (!$currentSlide.length) {
                $currentSlide = $centerSlide;
            }

            // выделяем активный слайд
            if ($currentSlide.length && (this.slider.$currentSlide.get(0) !== $currentSlide.get(0))) {
                this.slider._setCurrentSlide($currentSlide);
                this.slider._updateListHeight(this.opts.animateListHeight);
            }

            // =============================
            // Перемещаем слайды
            // =============================
            if (dragLeft) {
                if (!$rightSlide.length && !this.opts.dragBounds) {
                    // граничный слайд
                    slideOffset = 0;
                }

                $centerSlide.css({
                    transform: 'translate(' + (-slideOffset) + '%, 0%)'
                });
                $rightSlide.css({
                    transform: 'translate(' + (-slideOffset + slidesDistance) + '%, 0%)'
                });

                this._slides = [
                    $centerSlide.get(0),
                    $rightSlide.get(0)
                ];
                this._transforms = [
                    -slideOffset,
                    -slideOffset + slidesDistance
                ];
            } else {
                if (!$leftSlide.length && !this.opts.dragBounds) {
                    // граничный слайд
                    slideOffset = 0;
                }

                $leftSlide.css({
                    transform: 'translate(' + (slideOffset - slidesDistance) + '%, 0%)'
                });
                $centerSlide.css({
                    transform: 'translate(' + slideOffset + '%, 0%)'
                });

                this._slides = [
                    $leftSlide.get(0),
                    $centerSlide.get(0)
                ];
                this._transforms = [
                    slideOffset - slidesDistance,
                    slideOffset
                ];
            }
        };

        /*
            Завершение перетаскивания слайдов мышью или тачпадом
         */
        cls.onStopDrag = function() {
            if (!this._slides) {
                return
            }

            var slidesDistance = 100 + this._getPercentGap();

            var $leftSlide = $(this._slides[0]);
            var $rightSlide = $(this._slides[1]);
            var $currSlide = this.slider.$currentSlide;
            var isLeftCurrent = $currSlide.get(0) === $leftSlide.get(0);

            // определение анимации
            var state_from = {
                left_slide: this._transforms[0],
                right_slide: this._transforms[1]
            };
            if (isLeftCurrent) {
                var state_to = {
                    left_slide: 0,
                    right_slide: slidesDistance
                };
                var duration = Math.round(
                    this.opts.speed * Math.abs(state_from.left_slide) / slidesDistance
                );
            } else {
                state_to = {
                    left_slide: -slidesDistance,
                    right_slide: 0
                };
                duration = Math.round(
                    this.opts.speed * Math.abs(state_from.right_slide) / slidesDistance
                );
            }


            var that = this;
            this.slider._beforeSlide($currSlide);
            this.slider._animation = $(state_from).animate(state_to, {
                duration: Math.max(200, duration),
                easing: this.opts.easing,
                progress: function() {
                    $leftSlide.css({
                        transform: 'translate(' + this.left_slide + '%, 0%)'
                    });
                    $rightSlide.css({
                        transform: 'translate(' + this.right_slide + '%, 0%)'
                    });
                },
                complete: function() {
                    if (isLeftCurrent) {
                        $leftSlide.css({
                            transform: 'none'
                        });
                        $rightSlide.css({
                            transform: ''
                        });
                    } else {
                        $leftSlide.css({
                            transform: ''
                        });
                        $rightSlide.css({
                            transform: 'none'
                        });
                    }

                    that.slider.$list.css({
                        overflow: ''
                    });

                    that.slider._afterSlide($currSlide);
                }
            });

            this.slider.callPluginsMethod('stopDrag', null, true);
            this.slider.trigger('stopDrag');
        };
    });

})(jQuery);
