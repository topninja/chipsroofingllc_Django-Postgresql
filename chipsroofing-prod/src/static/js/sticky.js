(function($) {
    'use strict';

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.

        Зависит от:
            jquery-ui.js, jquery.utils.js, jquery.inspectors.js

        Параметры:
            blockSelector   - селектор родительского блока
            topOffset       - расстояние от верха окна до ползающего блока
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается

        Пример:
            <div id="block">
                <div class="sticky"></div>
                ...
            </div>

            $(document).ready(function() {
                $('.sticky').sticky();
            });
     */

    /** @namespace $window.scrollTop */

    var instances = [];
    var $window = $(window);
    $.widget("django.sticky", {
        options: {
            blockSelector: '',
            topOffset: 0,
            minEnabledWidth: 768,

            enable: function(event, data) {
                var that = data.widget;
                that._removeClass(that.element, 'sticky-disabled');
                that._addClass(that.element, 'sticky-enabled');
                that._setElementWidth();
                that.update();
            },
            disable: function(event, data) {
                var that = data.widget;
                that._addClass(that.element, 'sticky-disabled');
                that._removeClass(that.element, 'sticky-enabled');
                that.trigger('state', {
                    state: 'top'
                });
            },
            state: function(event, data) {
                var that = data.widget;
                var state = data.state;

                if (that._state !== state) {
                    that._state = state;
                }

                that.trigger('update', {
                    state: state,
                    offset: data.offset
                });
            },
            update: function(event, data) {
                var that = data.widget;
                var state = data.state;

                if (state === 'top') {
                    that.element.css({
                        position: '',
                        top: ''
                    });
                } else if (state === 'middle') {
                    that.element.css({
                        position: 'fixed',
                        top: that.options.topOffset
                    });
                } else if (state === 'bottom') {
                    that.element.css({
                        position: 'absolute',
                        top: data.offset
                    });
                }
            },
            resize: function(event, data) {
                var that = data.widget;
                that._setElementWidth();
                $.animation_frame(function() {
                    that._update(data.winScroll);
                })(that.element.get(0));
            },
            destroy: function(event, data) {
                var that = data.widget;
                that.element.css({
                    position: '',
                    top: '',
                    width: ''
                });
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
            if (this.block.css('position') === 'static') {
                this.block.css({
                    'position': 'relative'
                });
            }
            this.block.css('overflow', 'hidden');

            if (!this.element.hasClass('sticky')) {
                this._addClass('sticky');
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
            Фиксируем ширину ползающего блока
         */
        _setElementWidth: function() {
            var initial_css = this.element.get(0).style.cssText;

            this.element.get(0).style.cssText = '';
            this._width = this.element.width();
            this.element.get(0).style.cssText = initial_css;

            this.element.css('width', this._width);
        },

        /*
            Обновление положения
         */
        update: function() {
            var winScroll = $window.scrollTop();
            this._update(winScroll);
        },

        _update: function(winScroll) {
            if (this.options.disabled) {
                return
            }

            var paddingTop = (parseInt(this.block.css('padding-top')) || 0);
            var paddingBottom = (parseInt(this.block.css('padding-bottom')) || 0);

            var areaTop = this.block.offset().top;
            var areaHeight = this.block.outerHeight();

            var element_height = this.element.outerHeight(true);

            var scrollFrom = areaTop + paddingTop - this.options.topOffset;
            var scrollTo = scrollFrom + this.block.height() - element_height;

            if (winScroll < scrollFrom) {
                this.trigger('state', {
                    state: 'top',
                    offset: 0
                });
            } else if (this.block.height() > this.element.outerHeight(true)) {
                if (winScroll > scrollTo) {
                    this.trigger('state', {
                        state: 'bottom',
                        offset: areaHeight - element_height - paddingBottom
                    });
                } else if ((winScroll >= scrollFrom) && (winScroll <= scrollTo)) {
                    this.trigger('state', {
                        state: 'middle',
                        offset: paddingTop + winScroll - scrollFrom
                    });
                }
            }
        }
    });

    var updateStickies = function() {
        var winScroll = $window.scrollTop();
        $.each(instances, function(i, widget) {
            $.animation_frame(function() {
                widget._update(winScroll);
            })(widget.element.get(0));
        });
    };

    $window.on('scroll.sticky', updateStickies);
    $window.on('load.sticky', updateStickies);
    $window.on('resize.sticky', $.rared(function() {
        var winScroll = $window.scrollTop();
        $.each(instances, function(i, widget) {
            widget.trigger('resize', {
                winScroll: winScroll
            });
        });
    }, 100));

})(jQuery);
