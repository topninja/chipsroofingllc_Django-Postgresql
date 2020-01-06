(function($) {
    'use strict';

    window.SliderAutoscrollPlugin = Class(SliderPlugin, function SliderAutoscrollPlugin(cls, superclass) {
        cls.PLUGIN_NAME = 'autoscroll';

        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animationOptions: {
                animateListHeight: true
            },

            progress_interval: 40,
            interval: 3000,
            direction: 'next',          // next / prev / random
            stopOnHover: true,

            onProgress: $.noop,
            checkEnabled: function() {
                return this.slider.$slides.length >= 2;
            }
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }
        };

        cls.enable = function() {
            this.startTimer();
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.stopTimer();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            this.stopTimer();
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            if (this.opts.direction === 'prev') {
                this._timerHandler = $.proxy(
                    this.slider.slidePrevious,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animationOptions
                );
            } else if (this.opts.direction === 'next') {
                this._timerHandler = $.proxy(
                    this.slider.slideNext,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animationOptions
                );
            } else if (this.opts.direction === 'random') {
                this._timerHandler = $.proxy(
                    this.slider.slideRandom,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animationOptions
                );
            } else {
                this.error('Invalid direction: ' + this.opts.direction);
                return
            }

            this._total_steps = Math.ceil(this.opts.interval / this.opts.progress_interval);
            this._steps_done = 0;
            this._attachEvents();
            this._updateEnabledState();
        };

        /*
            Сброс таймера при изменении кол-ва слайдов
         */
        cls.onUpdateSlides = function() {
            this.stopTimer();
            this._updateEnabledState();
        };

        /*
            Сброс таймера при переключении слайда
         */
        cls.beforeSlide = function() {
            this.stopTimer();
        };

        cls.afterSlide = function() {
            if (this.enabled) {
                this._steps_done = 0;
                this.startTimer();
            }
        };

        /*
            Сброс таймера при перетаскивании
         */
        cls.startDrag = function() {
            this.stopTimer();
        };

        cls.stopDrag = function() {
            if (this.enabled) {
                this._steps_done = 0;
                this.startTimer();
            }
        };

        /*
            Навешивание событий
         */
        cls._attachEvents = function() {
            var that = this;
            if (this.opts.stopOnHover) {
                this.slider.$root.off('.autoscroll');
                this.slider.$root.on('mouseenter.slider.autoscroll', function() {
                    that.stopTimer();
                }).on('mouseleave.slider.autoscroll', function() {
                    that.startTimer();
                });
            }
        };

        /*
            Создание таймера
         */
        cls.startTimer = function() {
            if (!this.enabled) return;
            this.stopTimer();

            // инициализация
            this.opts.onProgress(this._steps_done / this._total_steps);

            var that = this;
            this._timer = setInterval(function() {
                that._steps_done += 1;
                if (that._steps_done >= that._total_steps) {
                    that._steps_done = 0;
                    that._timerHandler();
                }

                that.opts.onProgress(that._steps_done / that._total_steps);
            }, this.opts.progress_interval);
        };

        /*
            Остановка таймера
         */
        cls.stopTimer = function() {
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        };
    });

})(jQuery);
