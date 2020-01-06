(function() {
    'use strict';

    /*
        Эффект параллакса, зависящий от величины прокрутки страницы.

        Зависит от:
            jquery-ui.js, jquery.utils.js, jquery.inspectors.js

        Параметры:
            blockSelector   - селектор родительского блока
            easing          - функция сглаживания перемещения фона
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается

        Пример:
            // Двигаем блок внутри контейнера #ctnr.
            // Перемещение начинается от точки, когда контейнер становится видимым

            $('.layer').layer()
     */

    var instances = [];
    var $window = $(window);
    $.widget("django.layer", {
        options: {
            blockSelector: '',
            easing: 'easeInOutQuad',
            minEnabledWidth: 768,

            enable: function(event, data) {
                var that = data.widget;
                that._removeClass(that.element, 'layer-disabled');
                that._addClass(that.element, 'layer-enabled');
                that.update();
            },
            disable: function(event, data) {
                var that = data.widget;
                that._addClass(that.element, 'layer-disabled');
                that._removeClass(that.element, 'layer-enabled');
            },
            update: function(event, data) {
                var that = data.widget;
                var offset = data.progress * (data.blockHeight - that.element.outerHeight());
                that.element.css({
                    transform: 'translate3d(0%, ' + offset + 'px, 0)'
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
                that.element.css('transform', '');
            }
        },

        _create: function() {
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
            if (!this.block.hasClass('layer-block')) {
                this._addClass(this.block, 'layer-block');
            }

            if (!this.element.hasClass('layer')) {
                this._addClass('layer');
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
            $.mediaInspector.ignore(this.element);

            var index = instances.indexOf(this);
            if (index >= 0) {
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
            Обновление положения
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


    var updateLayers = function() {
        var winScroll = $window.scrollTop();
        var winHeight = $window.height();
        $.each(instances, function(i, widget) {
            $.animation_frame(function() {
                widget._update(winScroll, winHeight);
            })(widget.element.get(0));
        });
    };

    $window.on('scroll.layers', updateLayers);
    $window.on('load.layers', updateLayers);
    $window.on('resize.layers', $.rared(function() {
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
