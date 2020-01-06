(function($) {
    'use strict';

    /*
        Модуль слайдера с подключаемыми плагинами.

        Для упрощения стилизации кода слайдера для случаев, когда JS отключен
        или ещё не загружен, списку можно поставить класс "no-slider".
        Этот класс будет удален, когда слайдер будет готов.

        Требует:
            jquery.utils.js

        Параметры:
            rootClass                       - класс, добавляемый корневому элементу
            listWrapperClass                - класс, добавляемый обертке над списком
            listClass                       - класс, добавляемый списку
            slideClass                      - класс, добавляемый слайду
            slideActiveClass                - класс активного слайда
            itemClass                       - класс, добавляемый элементу списка
            initialActiveItemClass          - класс начально активного элемента

            itemSelector: str               - селектор элементов слайдера
            itemsPerSlide: number / func    - кол-во элементов на каждый слайд
            loop: bool                      - зацикленный слайдер

            // вариант установки высоты слайдера
            sliderHeight: str
                'current'  - по высоте текущего слайда
                'max'      - по высоте максимального слайда
                'none'     - не задавать высоту

            sliderHeightTransition          - длительность анимации высоты слайдера

        Методы:
            // получение текущего слайда
            getCurrentSlide()

            // получение следующего слайда
            getNextSlide()

            // получение предыдущего слайда
            getPreviousSlide()

            // подключение плагинов
            attachPlugins(plugin1, plugin2, ...)

            // перерасчет высоты слайдера
            updateListHeight(doAnimation)

            // обновление внутреннего списка слайдов
            updateSlides()

            // переход к слайду $toSlide с анимацией animationName
            slideTo($slide, animationName, options)

            // переход к следующему слайду
            slideNext(animationName, options)

            // переход к предыдущему слайду
            slidePrevious(animationName, options)

        События:
            changeSlide     - после изменения текущего слайда
            updateSlides    - после изменения кол-ва слайдов

            beforeSlide     - перед анимацией перехода к слайду
            afterSlide      - после анимации перехода к слайду

            startDrag       - начало перетаскивания слайдов
            stopDrag        - завершение перетаскивания слайдов

            resize          - изменение размера окна

        Примечания по событиям:
            1) при инициализации события не вызываются, т.к. их
               обработчики вы ещё не повесили :)

            2) changeSlide может вызываться без beforeSlide.
               Например, при перетаскивании слайда мышкой через несколько слайдов.


        HTML пример:
            <div class="slider no-slider">
                <div class="slider-item">...
                <div class="slider-item">
                ...
            </div>

        JS пример:
            Slider('.slider', {
                sliderHeight: Slider.prototype.HEIGHT_CURRENT,
                loop: false,
                itemsPerSlide: 2
            }).attachPlugins([
                SliderSideAnimation({
                    margin: 20
                }),
                SliderSideShortestAnimation({
                    margin: 20
                }),
                SliderFadeAnimation(),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    margin: 20
                }),
                SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 6000
                })
            ]);


        Пример динамического количества элементов в слайде:
            Slider('.slider', {
                itemsPerSlide: function() {
                    if ($.winWidth() >= 1200)  {
                        return 4
                    } else {
                        return 3
                    }
                }
            });
    */

    /** @namespace window.TweenLite */
    /** @namespace window.TimelineLite */
    var sliders = [];

    window.Slider = Class(EventedObject, function Slider(cls, superclass) {
        // варианты установки высоты слайдера
        cls.HEIGHT_CURRENT = 'current';    // по высоте текущего слайда
        cls.HEIGHT_MAX = 'max';            // по высоте максимального слайда
        cls.HEIGHT_NONE = 'none';          // не устанавливать высоту
        cls.HEIGHT_TYPES = [
            cls.HEIGHT_CURRENT,
            cls.HEIGHT_MAX,
            cls.HEIGHT_NONE
        ];

        cls.defaults = {
            rootClass: 'slider-root',
            listWrapperClass: 'slider-list-wrapper',
            listClass: 'slider-list',
            slideClass: 'slider-slide',
            slideActiveClass: 'slider-slide-active',
            itemClass: 'slider-item',
            initialActiveItemClass: 'active',

            itemSelector: '.slider-item',
            itemsPerSlide: 1,
            loop: true,
            sliderHeight: cls.HEIGHT_MAX,
            sliderHeightTransition: 800
        };

        cls.DATA_KEY = 'slider';
        cls.REMOVABLE_CLASS = 'no-slider';

        cls.init = function(list, options) {
            superclass.init.call(this);

            this.$list = $(list).first();
            if (!this.$list.length) {
                return this.raise('list element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // плагины
            this._plugins = [];
            this.attachPlugins(SliderInstantAnimation());

            // добавляем класс на список
            this.$list.addClass(this.opts.listClass);

            // создание обертки списка
            this.$listWrapper = this.$list.closest('.' + this.opts.listWrapperClass);
            if (!this.$listWrapper.length) {
                this.$list.wrap('<div>');
                this.$listWrapper = this.$list.parent().addClass(this.opts.listWrapperClass);
            }

            // создание корневого элемента слайдера
            this.$root = this.$listWrapper.closest('.' + this.opts.rootClass);
            if (!this.$root.length) {
                this.$listWrapper.wrap('<div>');
                this.$root = this.$listWrapper.parent().addClass(this.opts.rootClass);
            }

            // сохраняем массив items
            this.$items = this.$list.find(this.opts.itemSelector);
            this.$items.addClass(this.opts.itemClass);

            if (!this.$items.length) {
                return this.raise('there are no items in list');
            }

            // объект анимации
            this._animation = null;

            // текущий элемент
            this.$currentItem = this.$items.filter('.' + this.opts.initialActiveItemClass).first();
            if (!this.$currentItem.length) {
                this.$currentItem = this.$items.first();
            }

            // создаем слайды
            this.$currentSlide = $();
            this.setItemsPerSlide(this.opts.itemsPerSlide);

            // обновление высоты по мере загрузки картинок
            var $images;
            if (this.opts.sliderHeight === this.HEIGHT_CURRENT) {
                $images = this.$currentSlide.find('img');
            } else if (this.opts.sliderHeight === this.HEIGHT_MAX) {
                $images = this.$list.find('img');
            } else if (this.opts.sliderHeight === this.HEIGHT_NONE) {
                $images = $();
            } else {
                return this.raise('unknown sliderHeight');
            }

            if ($images && $images.length) {
                var that = this;
                var loadHandle = $.rared(function() {
                    that.updateListHeight();
                }, 100);

                $images.on('load', loadHandle);
            }

            this.$list.removeClass(this.REMOVABLE_CLASS);
            this.$list.data(this.DATA_KEY, this);
            this.updateListHeight();

            sliders.push(this);
        };

        cls.stopAnimation = function(jumpToEnd) {
            if (!this._animation) return;

            if ((window.TweenLite && (this._animation instanceof TweenLite)) || (window.TweenMax && (this._animation instanceof TweenMax))) {
                this._animation.totalProgress(1);
            } else if ((window.TimelineLite && (this._animation instanceof TimelineLite)) || (window.TimelineMax && (this._animation instanceof TimelineMax))) {
                this._animation.totalProgress(1);
            } else {
                this._animation.stop(true, jumpToEnd);
            }

            this._animation = null;
            this._animation_name = null;
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // Прерывание анимации, если она запущена
            this.stopAnimation(true);
            this.callPluginsMethod('destroy');
            this.$list.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        // ===============================================
        // ================ current slide ================
        // ===============================================

        /*
            Получение активного слайда
         */
        cls.getCurrentSlide = function() {
            return this.$currentItem.closest('.' + this.opts.slideClass);
        };

        /*
            Изменение текущего слайда
         */
        cls._setCurrentSlide = function($slide) {
            if (!$slide || !$slide.length || (this.$slides.index($slide) < 0)) {
                return false
            }

            var $old_slide = this.$currentSlide;
            if ($old_slide.length && ($old_slide.get(0) === $slide.get(0))) {
                return false
            }

            $old_slide.removeClass(this.opts.slideActiveClass);
            $slide.addClass(this.opts.slideActiveClass);

            this.$currentItem = $slide.find('.' + this.opts.itemClass).first();
            this.$currentSlide = $slide;
            this._onChangeSlide($slide, $old_slide);
        };

        cls._onChangeSlide = function($slide, $old_slide) {
            this.callPluginsMethod('onChangeSlide', [$slide, $old_slide], true);
            this.trigger('changeSlide', $slide, $old_slide);
        };

        // ===============================================
        // ================ create slides ================
        // ===============================================

        /*
            Создание слайдов, содержащих по itemsPerSlide элементов в каждом слайде.
            В каждом плагине вызывает метод onUpdateSlides.
         */
        cls.setItemsPerSlide = function(itemsPerSlide) {
            // рассчет и форматирование
            if ($.isFunction(itemsPerSlide)) {
                var new_ips = parseInt(itemsPerSlide.call(this));
            } else {
                new_ips = parseInt(itemsPerSlide);
            }

            if (!new_ips || (new_ips < 1)) {
                return
            }

            // значение изменилось или нет?
            var old_ips = this._itemsPerSlide;
            if (old_ips === new_ips) {
                return
            } else {
                this._itemsPerSlide = new_ips;
            }

            this.stopAnimation(true);

            // сохраняем элементы, удалив их из DOM
            var $items = this.$items.detach();

            // удаляем ранее созданные слайды
            this.$list.find('.' + this.opts.slideClass).remove();

            // создаем новые слайды
            var slide_count = Math.ceil($items.length / this._itemsPerSlide);
            for (var i = 0; i < slide_count; i++) {
                var $slide = $('<div>').addClass(this.opts.slideClass);
                this.$list.append(
                    $slide.append(
                        $items.slice(i * this._itemsPerSlide, (i + 1) * this._itemsPerSlide)
                    )
                );
            }

            // обновляем кол-во слайдов
            this.updateSlides();
        };

        /*
            Обновление кол-ва слайдов
         */
        cls.updateSlides = function() {
            this.$slides = this.$list.find('.' + this.opts.slideClass);

            this.callPluginsMethod('onUpdateSlides');
            this.trigger('updateSlides');

            // мгновенный переход к активному слайду
            this.slideTo(this.getCurrentSlide());
        };

        // ===============================================
        // ============== plugin methods =================
        // ===============================================

        /*
            Подключение плагинов
         */
        cls.attachPlugins = function(plugins) {
            var that = this;
            if ($.isArray(plugins)) {
                $.each(plugins, function(index, plugin) {
                    if (plugin instanceof window.SliderPlugin) {
                        that._plugins.push(plugin);
                        plugin.onAttach(that);
                    }
                });
            } else if (plugins instanceof window.SliderPlugin) {
                this._plugins.push(plugins);
                plugins.onAttach(this);
            }
            return this;
        };

        /*
            Поиск реализации метода среди плагинов
         */
        cls.getPluginMethod = function(pluginName, methodName) {
            if (!methodName) {
                this.warn('methodName required');
            }

            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if ((plugin.PLUGIN_NAME === pluginName) && $.isFunction(plugin[methodName])) {
                    return $.proxy(plugin[methodName], plugin);
                }
            }

            this.warn('Not found method "' + methodName + '" in plugin "' + pluginName + '"');
        };

        /*
            Вызов метода methodName с агрументами args во всех плагинах,
            в которых этот метод реализован.

            Если reversed=true, обход плагинов будет в обратном порядке
         */
        cls.callPluginsMethod = function(methodName, args, reversed) {
            var plugins = this._plugins.concat();
            if (reversed) {
                plugins.reverse();
            }

            var index = plugins.length;
            while (index--) {
                var plugin = plugins[index];
                if (methodName in plugin) {
                    plugin[methodName].apply(plugin, args);
                }
            }
        };

        // ===============================================
        // ================= update height ===============
        // ===============================================

        /*
            Рассчет высоты слайдера
         */
        cls.calcListHeight = function() {
            if (this.opts.sliderHeight === cls.HEIGHT_CURRENT) {
                return this.$currentSlide.outerHeight();
            } else if (this.opts.sliderHeight === cls.HEIGHT_MAX) {
                var final_height = 0;
                this.$slides.height('auto');
                $.each(this.$slides, function(i, slide) {
                    var $slide = $(slide);
                    var height = $slide.outerHeight();
                    if (height > final_height) {
                        final_height = height;
                    }
                });
                this.$slides.height('');
                return final_height;
            }
        };

        /*
            Обновление высоты slider.$list в зависимости от высоты слайдов
         */
        cls.updateListHeight = function(doAnimation) {
            // прерываем анимацию высоты, если она идёт
            if (this._list_height_animation) {
                this._list_height_animation.stop(true);
                this._list_height_animation = null;
            }

            var that = this;
            $.animation_frame(function() {
                var final_height = parseInt(that.calcListHeight());
                if (isNaN(final_height)) {
                    return;
                }

                // высота не меняется - выходим
                var current_height = that.$list.height();
                if (current_height === final_height) {
                    return
                }

                that._beforeUpdateListHeight(current_height, final_height);
                if (doAnimation && that.opts.sliderHeightTransition) {
                    // с анимацией
                    that._list_height_animation = $({
                        height: current_height
                    }).animate({
                        height: final_height
                    }, {
                        duration: that.opts.sliderHeightTransition,
                        easing: 'easeOutCubic',
                        progress: function () {
                            that.$list.css('height', this.height);
                        },
                        complete: function() {
                            that._afterUpdateListHeight(current_height, final_height);
                        }
                    });
                } else {
                    // мгновенно
                    that.$list.height(final_height);
                    that._afterUpdateListHeight(current_height, final_height);
                }
            })();
        };

        /*
            Обновление высоты слайдера по условию
         */
        cls._updateListHeight = function(doAnimation) {
            if (this.opts.sliderHeight === cls.HEIGHT_CURRENT) {
                this.updateListHeight(doAnimation);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        cls._beforeUpdateListHeight = function(current, final) {
            this.callPluginsMethod('beforeUpdateListHeight', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        cls._afterUpdateListHeight = function(current, final) {
            this.callPluginsMethod('afterUpdateListHeight', arguments, true);
        };


        /*
            Метод, вызываемый при изменении размера окна браузера
         */
        cls.onResize = function() {
            this.callPluginsMethod('onResize');

            // обновление кол-ва элементов в слайдах
            this.setItemsPerSlide(this.opts.itemsPerSlide);
            this.trigger('resize');
            this.updateListHeight();
        };

        // ===============================================
        // =============== slides methods ================
        // ===============================================

        /*
            Метод, возвращающий следующий слайд.
         */
        cls.getNextSlide = function($fromSlide) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            var slides_count = this.$slides.length;
            var index = this.$slides.index($fromSlide) + 1;

            if (index < slides_count) {
                return this.$slides.eq(index);
            } else if (this.opts.loop) {
                return this.$slides.eq(index % slides_count);
            } else {
                return $();
            }
        };

        /*
            Метод, возвращающий предыдущий слайд.
         */
        cls.getPreviousSlide = function($fromSlide) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            var slides_count = this.$slides.length;
            var index = this.$slides.index($fromSlide) - 1;

            if (index >= 0) {
                return this.$slides.eq(index);
            } else if (this.opts.loop) {
                return this.$slides.eq(index % slides_count);
            } else {
                return $();
            }
        };

        // ===============================================
        // =============== slide animation ===============
        // ===============================================

        /*
            Метод смены текущего слайда на $toSlide.

            Объект анимации (если он есть) НЕОБХОДИМО сохранить в переменной
            this.slider._animation.

            При реализации этого метода в плагинах, НЕОБХОДИМО вызывать
            методы слайдера _beforeSlide, _setCurrentSlide, _afterSlide и _updateListHeight.

            Пример:
                this.slider._beforeSlide($slide);
                this.slider._setCurrentSlide($slide);
                ....
                var that = this;
                this.slider._animation = $(...).animate({
                    ...
                }, {
                    ...
                    complete: function() {
                        ...
                        that.slider._afterSlide($slide);
                    }
                })
         */
        cls.slideTo = function($slide, animationName, options) {
            if (!$slide || !$slide.length || (this.$slides.index($slide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide && (this.$currentSlide.get(0) === $slide.get(0))) {
                return
            }

            animationName = animationName || 'instant';
            var method = this.getPluginMethod(animationName, 'slideTo');
            if (method) {
                method($slide, $.extend({
                    animateListHeight: false
                }, options));
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед анимацией изменения текущего слайда (любым из плагинов).
         */
        cls._beforeSlide = function($slide) {
            this.trigger('beforeSlide', $slide);
            this.callPluginsMethod('beforeSlide', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            после завершения анимации изменения текущего слайда (любым из плагинов).
         */
        cls._afterSlide = function($slide) {
            this.callPluginsMethod('afterSlide', arguments, true);
            this.trigger('afterSlide', $slide);
        };

        cls.slideNext = function(animationName, options) {
            var $slide = this.getNextSlide();
            this.slideTo($slide, animationName, options);
        };

        cls.slidePrevious = function(animationName, options) {
            var $slide = this.getPreviousSlide();
            this.slideTo($slide, animationName, options);
        };

        cls.slideRandom = function(animationName, options) {
            var slides_count = this.$slides.length;
            var random_index = Math.floor(Math.random() * (slides_count - 1));
            var current_index = this.$slides.index(this.$currentSlide);
            var final_index = (random_index < current_index) ? random_index : random_index + 1;

            var $slide = this.$slides.eq(final_index);
            this.slideTo($slide, animationName, options);
        };
    });


    // ================================================
    //            Базовый класс плагина
    // ================================================
    window.SliderPlugin = Class(Object, function SliderPlugin(cls, superclass) {
        cls.defaults = {
            checkEnabled: $.noop
        };

        cls.init = function(settings) {
            this.opts = $.extend(true, {}, this.defaults, settings);
        };

        cls.destroy = function() {
            var plugin_index = this.slider._plugins.indexOf(this);
            if (plugin_index >= 0) {
                this.slider._plugins.splice(plugin_index, 1);
            }
        };

        // Инициализация
        cls.onAttach = function(slider) {
            this.slider = slider;
        };

        // Событие изменения размера окна
        cls.onResize = function() {

        };

        /*
            Проверка включенности и включение / выключение
         */
        cls._updateEnabledState = function() {
            var status = this.opts.checkEnabled.call(this) !== false;
            if (this.enabled === status) return;

            this.enabled = status;
            if (this.enabled) {
                this.enable();
            } else {
                this.disable();
            }
        };

        // Включение
        cls.enable = function() {
            this.enabled = true;
        };

        // Выключение
        cls.disable = function() {
            this.enabled = false;
        };
    });

    // ================================================
    //          Базовый плагин анимации
    // ================================================
    window.SliderAnimationPlugin = Class(window.SliderPlugin, function SliderAnimationPlugin(cls, superclass) {
        cls.slideTo = function($slide, options) {
            this.stopAnimation();

            var $currentSlide = this.slider.$currentSlide;
            var $targetSlide = $slide;

            this.animationOptions = this.buildAnimationOptions(options);
            this.prepareAnimation($currentSlide, $targetSlide);

            this.slider._beforeSlide($targetSlide);
            this.slider._setCurrentSlide($targetSlide);
            this.startAnimation($currentSlide, $targetSlide);
            this.slider._updateListHeight(this.animationOptions.animateListHeight);
        };

        /*
            Построение настроек анимации.
            Учитывает опции, переданные через slider.slideTo()
         */
        cls.buildAnimationOptions = function(options) {
            return $.extend({
                animateListHeight: false
            }, options);
        };

        /*
            Остановка предыдущей анимации
         */
        cls.stopAnimation = function() {
            this.slider.stopAnimation(true);
        };

        /*
            Подготовка слайдов к анимации
         */
        cls.prepareAnimation = function($currentSlide, $targetSlide) {

        };

        /*
            Запуск анимации.
            При окончании анимации необходимо вызвать метод endAnimation.
         */
        cls.startAnimation = function($currentSlide, $targetSlide) {
            this.slider._animation_name = this.PLUGIN_NAME;
        };

        /*
            Callback завершения анимации
         */
        cls.endAnimation = function($currentSlide, $targetSlide) {
            this.slider._afterSlide($targetSlide);
            this.slider._animation = null;
            this.slider._animation_name = null;
        };
    });

    // ================================================
    //          Плагин мгновенной анимации
    // ================================================
    window.SliderInstantAnimation = Class(window.SliderAnimationPlugin, function SliderInstantAnimation(cls, superclass) {
        cls.PLUGIN_NAME = 'instant';

        cls.startAnimation = function($currentSlide, $targetSlide) {
            superclass.startAnimation.call(this, $currentSlide, $targetSlide);
            $currentSlide.css({
                transform: ''
            });
            $targetSlide.css({
                transform: 'none'
            });
            this.endAnimation($currentSlide, $targetSlide);
        };
    });

    // Обновление высоты слайдера
    $(window).on('load.slider', function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight();
        });

        // fallback
        var counter = 10;
        var interval = setInterval(function() {
            $.each(sliders, function(i, slider) {
                if (!slider._list_height_animation) {
                    slider.updateListHeight();
                }
            });

            if (--counter === 0) {
                clearInterval(interval);
            }
        }, 2000);
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.onResize();
        });
    }, 100));

})(jQuery);
