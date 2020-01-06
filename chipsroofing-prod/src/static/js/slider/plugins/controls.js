(function($) {
    'use strict';

    window.SliderControlsPlugin = Class(SliderPlugin, function SliderControlsPlugin(cls, superclass) {
        cls.PLUGIN_NAME = 'controls';

        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animationOptions: {
                animateListHeight: true
            },

            arrowClass: 'slider-arrow',
            arrowLeftClass: 'slider-arrow-left',
            arrowRightClass: 'slider-arrow-right',
            arrowDisabledClass: 'slider-arrow-disabled',

            container: null,
            disableOnBounds: true
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }

            // создание кнопок
            this._createDOM();
        };

        cls.enable = function() {
            this.$left.css('display', '');
            this.$right.css('display', '');
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.$left.hide();
            this.$right.hide();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            this.$left.remove();
            this.$right.remove();
            this.$left = null;
            this.$right = null;
            superclass.destroy.call(this);
        };

        /*
            Создание стрелок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this._attachDOM();
            this._attachEvents();
            this.checkBounds();
            this._updateEnabledState();
        };

        cls.onUpdateSlides = function() {
            this.checkBounds();
            this._updateEnabledState();
        };

        /*
            Деактивируем стрелки на границах сладера
         */
        cls.onChangeSlide = function() {
            this.checkBounds();
        };

        /*
            Создание DOM-элементов стрелок
         */
        cls._createDOM = function() {
            this.$left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .append('<span>');

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .append('<span>');
        };

        /*
            Навешивание событий
         */
        cls._attachEvents = function() {
            this.$left.off('.controls');
            this.$right.off('.controls');

            var that = this;
            this.$left.on('click.slider.controls', function() {
                if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                    return false
                }

                that.slider.slidePrevious(
                    that.opts.animationName,
                    that.opts.animationOptions
                );
            });
            this.$right.on('click.slider.controls', function() {
                if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                    return false
                }

                that.slider.slideNext(
                    that.opts.animationName,
                    that.opts.animationOptions
                );
            });
        };

        /*
            Добавление кнопок в DOM-дерево
         */
        cls._attachDOM = function() {
            this.getContainer().append(this.$left, this.$right);
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
            Проверка и деактивация кнопок на границах
         */
        cls.checkBounds = function() {
            if (!this.opts.disableOnBounds) {
                return
            }

            var $curr = this.slider.$currentSlide;
            var $prev = this.slider.getPreviousSlide($curr);
            if (!$prev || !$prev.length || ($curr.get(0) === $prev.get(0))) {
                this.$left.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$left.removeClass(this.opts.arrowDisabledClass)
            }

            var $next = this.slider.getNextSlide($curr);
            if (!$next || !$next.length || ($curr.get(0) === $next.get(0))) {
                this.$right.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$right.removeClass(this.opts.arrowDisabledClass)
            }
        };
    });

})(jQuery);
