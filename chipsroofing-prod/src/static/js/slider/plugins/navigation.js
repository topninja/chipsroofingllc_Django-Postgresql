(function($) {
    'use strict';

    window.SliderNavigationPlugin = Class(SliderPlugin, function SliderNavigationPlugin(cls, superclass) {
        cls.PLUGIN_NAME = 'navigation';

        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animationOptions: {
                animateListHeight: true
            },

            wrapperClass: 'slider-navigation',
            windowClass: 'slider-navigation-window',
            itemClass: 'slider-navigation-item',
            activeItemClass: 'active',

            container: null,
            checkEnabled: function() {
                return this.slider.$slides.length >= 2
            }
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            this._createDOM();
        };

        cls.enable = function() {
            this.$wrapper.css('display', '');
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.$wrapper.hide();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            this.$wrapper.remove();
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this._attachDOM();
            this._attachEvents();
            this.updateNavigationItems();
            this.activateNavigationItem();
            this._updateEnabledState();
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.onUpdateSlides = function() {
            this.updateNavigationItems();
            this.activateNavigationItem();
            this._updateEnabledState();
        };

        /*
            Установка активной кнопки после установки активного слайда
         */
        cls.onChangeSlide = function() {
            this.activateNavigationItem();
        };

        /*
            Создание DOM-элементов стрелок
         */
        cls._createDOM = function() {
            this.$wrapper = $('<div>').addClass(this.opts.wrapperClass);
            this.$window = $('<div/>').addClass(this.opts.windowClass);
            this.$window.appendTo(this.$wrapper);
        };

        /*
            Навешивание событий
         */
        cls._attachEvents = function() {
            var that = this;
            if (this.opts.animationName) {
                this.$wrapper.off('.navigation');
                this.$wrapper.on('click.slider.navigation', '.' + this.opts.itemClass, function() {
                    var slideIndex = $(this).data('slideIndex') || 0;
                    that.slider.slideTo(
                        that.slider.$slides.eq(slideIndex),
                        that.opts.animationName,
                        that.opts.animationOptions
                    );
                });
            }
        };

        /*
            Добавление кнопок в DOM-дерево
         */
        cls._attachDOM = function() {
            this.getContainer().append(this.$wrapper);
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
                $container = this.slider.$root;
            } else if ($container.length) {
                $container = $container.first();
            }

            return $container;
        };

        /*
            Обновление кол-ва кнопок в DOM
         */
        cls.updateNavigationItems = function() {
            // удаление старых точек навигации
            this.$wrapper.find('.' + this.opts.itemClass).remove();

            var that = this;
            $.each(this.slider.$slides, function(index) {
                var $item = $('<a>').addClass(that.opts.itemClass).data('slideIndex', index);
                $item.append($('<span>').text(index + 1));
                that.$window.append($item);
            });
        };

        /*
            Активация текущей кнопки
         */
        cls.activateNavigationItem = function() {
            var $slide = this.slider.$currentSlide;
            var slideIndex = this.slider.$slides.index($slide);
            var $item = this.$wrapper.find('.' + this.opts.itemClass).eq(slideIndex);

            $item.addClass(this.opts.activeItemClass);
            $item.siblings('.' + this.opts.itemClass).removeClass(this.opts.activeItemClass);
        };
    });


    /*
        Сокращенная по ширине навигация, которая скроллится при изменении текущего слайда.
        На граничные точки навешиваются дополнительные классы: "small-dot" и "smaller-dot".
     */
    window.SliderScrollableNavigationPlugin = Class(window.SliderNavigationPlugin, function SliderScrollableNavigationPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            wrapperClass: 'slider-navigation slider-scrollable-navigation',
            maxEnabledWidth: 640,
            maxItems: 5
        });

        /*
            Проверка, нужно ли сжимать навигацию
         */
        cls._checkScrollable = function() {
            var winWidth = $.winWidth();
            var old_state = this.scrollable;
            this.scrollable = !this.opts.maxEnabledWidth || (winWidth < this.opts.maxEnabledWidth);
            if (this.scrollable === old_state) {
                return
            }

            if (this.scrollable) {
                this.$window.css({
                    whiteSpace: 'nowrap'
                });
            } else {
                this.$window.css({
                    whiteSpace: ''
                });
            }
        };

        cls._addClasses = function($slide) {
            var $dots = this.$wrapper.find('.' + this.opts.itemClass);
            $dots.removeClass('small-dot').removeClass('smaller-dot');

            var dot_count = $dots.length;
            if (dot_count <= this.opts.maxItems) {
                return
            }

            if (!this.scrollable) {
                return
            }

            var half = Math.ceil(this.opts.maxItems / 2);
            var slideIndex = this.slider.$slides.index($slide);
            if (slideIndex < half) {
                // начало последовательности
                $dots.eq(this.opts.maxItems - 2).addClass('small-dot').nextAll().addClass('smaller-dot');
            } else if (slideIndex >= (dot_count - half)) {
                // конец последовательности
                $dots.eq(dot_count - this.opts.maxItems + 1).addClass('small-dot').prevAll().addClass('smaller-dot');
            } else {
                $dots.eq(slideIndex + half - 2).addClass('small-dot').nextAll().addClass('smaller-dot');
                $dots.eq(slideIndex - half + 2).addClass('small-dot').prevAll().addClass('smaller-dot');
            }
        };

        /*
            Центрирование навигации
         */
        cls._centrizeWindow = function($slide, instant) {
            var slideIndex = this.slider.$slides.index($slide);
            var $item = this.$wrapper.find('.' + this.opts.itemClass).eq(slideIndex);
            var itemLeft = $item.offset().left + this.$wrapper.scrollLeft() - this.$wrapper.offset().left;
            var itemMarginLeft = parseFloat($item.css('marginLeft')) || 0;
            var itemCenterLeft = itemLeft - itemMarginLeft + $item.outerWidth(true) / 2;
            var offset = Math.max(0, itemCenterLeft - this.$wrapper.outerWidth() / 2);

            if (instant) {
                this.$wrapper.stop(true, false).scrollLeft(offset);
            } else {
                this.$wrapper.stop(true, false).animate({
                    scrollLeft: offset
                }, 500);
            }
        };

        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this._checkScrollable();
            this._addClasses(slider.$currentSlide);
        };

        cls.onUpdateSlides = function() {
            superclass.onUpdateSlides.call(this);
            this._addClasses(this.slider.$currentSlide);

            var that = this;
            setTimeout(function () {
                that._centrizeWindow(that.slider.$currentSlide, true);
            }, 0);
        };

        cls.beforeSlide = function($slide) {
            this._addClasses($slide);
            this._centrizeWindow($slide);
        };

        cls.onResize = function() {
            superclass.onResize.call(this);
            this._checkScrollable();
            this._addClasses(this.slider.$currentSlide);
        }
    });

})(jQuery);
