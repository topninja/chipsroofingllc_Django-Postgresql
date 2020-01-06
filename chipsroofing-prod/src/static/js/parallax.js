(function() {
    'use strict';

    /*
        Параллакс-эффект для блока.

        Зависит от:
            jquery-ui.js, jquery.utils.js, jquery.inspectors.js

        Параметры:
            blockSelector       - селектор родительского блока
            imageHeightPercents - высота фоновой картинки в процентах относительно высоты блока
            easing              - функция сглаживания перемещения фона
            minEnabledWidth     - минимальная ширина экрана, при которой элемент перемещается

        Пример:
            <div id="block">
                <img class="parallax" src="/img/bg.jpg">
                ...
            </div>

            $(document).ready(function() {
                $('.parallax').parallax();
            });
     */

    var instances = [];
    var $window = $(window);
    $.widget("django.parallax", {
        options: {
            blockSelector: '',
            imageHeightPercents: 150,
            minEnabledWidth: 768,
            easing: 'easeInOutQuad',

            imageloaded: function(event, data) {
                var that = data.widget;
                that._addClass('parallax-loaded');
            },
            enable: function(event, data) {
                var that = data.widget;
                that._removeClass(that.image, 'parallax-disabled');
                that._addClass(that.image, 'parallax-enabled');
                that.update();
            },
            disable: function(event, data) {
                var that = data.widget;
                that._addClass(that.image, 'parallax-disabled');
                that._removeClass(that.image, 'parallax-enabled');
            },
            update: function(event, data) {
                var that = data.widget;
                var backgroundOffset = data.progress * (1 - that.options.imageHeightPercents/100);
                that.image.css({
                    transform: 'translate(-50%, ' + (data.blockHeight * backgroundOffset) + 'px)'
                });
            },
            resize: function(event, data) {
                var that = data.widget;
                $.animation_frame(function() {
                    that._update(data.winScroll, data.winHeight);
                })(that.element.get(0));
            },
            destroy: function(event, data) {
                var that = data.widget;
                that.image.css({
                    width: '',
                    height: '',
                    transform: ''
                });
            }
        },

        _create: function() {
            // проверка тэга
            this.is_picture = this.element.prop('tagName') === 'PICTURE';
            if (this.is_picture) {
                this.image = this.element.find('img');
            } else {
                this.image = this.element;
            }

            // нахождение контейнера
            this.block = this._getBlock();

            // стилизация
            this._setStyles();

            // запуск
            this._updateEnabledState();

            // Включение и выключение параллакса в зависимости от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.element, {
                point: this.options.minEnabledWidth,
                afterCheck: function($element, opts, state) {
                    var old_state = this.getState($element);
                    if (state === old_state) {
                        return
                    }

                    if (state) {
                        that.enable();
                    } else {
                        that.disable()
                    }
                }
            });

            // инспектирование пропорций
            $.bgInspector.inspect(this.image, {
                checkOnInit: false,
                afterCheck: function($element, opts, state) {
                    if (state) {
                        // картинка шире
                        if (that.options.disabled) {
                            $element.css({
                                width: '',
                                height: '100.5%'
                            });
                        } else {
                            $element.css({
                                width: '',
                                height: that.options.imageHeightPercents + '%'
                            })
                        }
                    } else {
                        // картинка выше
                        if (that.options.disabled) {
                            $element.css({
                                width: '100.5%',
                                height: ''
                            })
                        } else {
                            var elem_asp = $element.data('bginspector_aspect');
                            var block_asp = that.block.data('bginspector_aspect');

                            var relation = 100 * (block_asp / elem_asp);
                            if (relation > that.options.imageHeightPercents) {
                                $element.css({
                                    width: '100.5%',
                                    height: ''
                                })
                            } else {
                                $element.css({
                                    width: 100 * that.options.imageHeightPercents / relation + '%',
                                    height: ''
                                })
                            }
                        }
                    }
                }
            });

            // Событие загрузки картинки
            this.image.onLoaded(true, function() {
                that.trigger('imageloaded');
                $.bgInspector.check(that.image);
                that.update();
            });

            instances.push(this);
        },

        /*
            Получение элемента контейнера
         */
        _getBlock: function() {
            if (this.options.blockSelector) {
                return this.element.closest(this.options.blockSelector);
            } else {
                return this.element.parent();
            }
        },

        /*
            Стилизация
         */
        _setStyles: function() {
            if (this.block.css('position') === 'static') {
                this.block.css({
                    'position': 'relative'
                })
            }
            this.block.css('overflow', 'hidden');

            if (!this.element.hasClass('parallax')) {
                this._addClass('parallax');
            }

            if (!this.image.hasClass('parallax-image')) {
                this._addClass(this.image, 'parallax-image');
            }
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._updateEnabledState();
        },

        _updateEnabledState: function() {
            if (this.options.disabled) {
                this.trigger('disable');
            } else {
                this.trigger('enable');
            }
        },

        _destroy: function() {
            this.block.css({
                position: '',
                overflow: ''
            });
            $.mediaInspector.ignore(this.element);
            $.bgInspector.ignore(this.image);

            var index = instances.indexOf(this);
            if (index>=0) {
                instances.splice(index, 1);
            }

            this.trigger('destroy');
        },


        /*
            Вызов событий
         */
        trigger: function(type, data) {
            this._trigger(type, null, $.extend({
                widget: this
            }, data));
        },

        /*
            Обновление положения изображения
         */
        update: function() {
            var winScroll = $window.scrollTop();
            var winHeight = $window.height();
            this._update(winScroll, winHeight);
        },

        _update: function(winScroll, winHeight) {
            if (this.options.disabled) {
                return
            }

            var blockTop = this.block.offset().top;
            var blockHeight = this.block.outerHeight();

            var scrollFrom = Math.max(0, blockTop - winHeight);
            var scrollTo = blockTop + blockHeight;
            if ((winScroll < scrollFrom) || (winScroll > scrollTo)) {
                return
            }

            var scrollLength = scrollTo - scrollFrom;
            var scrollPosition = (winScroll - scrollFrom) / scrollLength;
            var eProgress = $.easing[this.options.easing](scrollPosition);

            this.trigger('update', {
                blockTop: blockTop,
                blockHeight: blockHeight,
                winScroll: winScroll,
                winHeight: winHeight,
                scrollFrom: scrollFrom,
                scrollTo: scrollTo,
                scrollLength: scrollLength,
                scrollPosition: scrollPosition,
                progress: eProgress
            });
        }
    });


    var updateParallaxes = function() {
        var winScroll = $window.scrollTop();
        var winHeight = $window.height();
        $.each(instances, function(i, widget) {
            $.animation_frame(function() {
                widget._update(winScroll, winHeight);
            })(widget.element.get(0));
        });
    };

    $window.on('scroll.parallax', updateParallaxes);
    $window.on('load.parallax', updateParallaxes);
    $window.on('resize.parallax', $.rared(function() {
        var winScroll = $window.scrollTop();
        var winHeight = $window.height();
        $.each(instances, function(i, widget) {
            widget.trigger('resize', {
                winScroll: winScroll,
                winHeight: winHeight
            });
        });
    }, 100));

})(jQuery);
