(function() {
    'use strict';

    /*
        Сворачивание / разворачивание блока, представленного в двух версиях.

        Зависит от:
            jquery-ui.js

        Параметры:
            shortBlockSelector  - селектор краткой версии
            fullBlockSelector   - селектор полной версии
            buttonSelector      - селектор кнопок, которые сворачиают / разворачивают блок
            hiddenClass         - класс скрытого блока
            speed               - скорость сворачивания / разворачивания на 500 пикселей
            easing              - функция сглаживания сворачивания

        Пример:
            <div id="text-block">
                <div class="expander-short">...</div>
                <div class="expander-full hidden">...</div>
                <a href="#" class="expander-btn">read more</a>
            </div>

            $(document).ready(function() {
                $('#text-block').expander();
            });
     */

    $.widget("django.expander", {
        options: {
            shortBlockSelector: '.expander-short',
            fullBlockSelector: '.expander-full',
            buttonSelector: '.expander-btn',
            hiddenClass: 'hidden',

            speed: 800,
            easing: 'easeOutSine',

            enable: $.noop,
            disable: $.noop,
            destroy: $.noop,
            before_expand: $.noop,
            after_expand: $.noop,
            before_reduce: $.noop,
            after_reduce: $.noop
        },

        _create: function() {
            // нахождение краткого и полного вариантов блока
            this.short_block = this._getShortBlock();
            this.full_block = this._getFullBlock();

            if (!this.short_block.length || !this.full_block.length) {
                return;
            }

            // текущее состояние
            this._expanded = this.short_block.hasClass(this.options.hiddenClass);
            if (this._expanded) {
                this.full_block.removeClass(this.options.hiddenClass);
            } else {
                this.full_block.addClass(this.options.hiddenClass);
            }

            // стилизация
            this._setStyles();

            // запуск
            this._updateEnabledState();

            // клик на кнопку
            var that = this;
            var events = {};
            events['click ' + this.options.buttonSelector] = function(event) {
                if (that._expanded) {
                    that.reduce($(event.currentTarget));
                } else {
                    that.expand($(event.currentTarget));
                }
                return false
            };
            this._on(events);
        },

        /*
            Получение краткого варианта блока
         */
        _getShortBlock: function() {
            return this.element.find(this.options.shortBlockSelector);
        },

        /*
            Получение полного варианта блока
         */
        _getFullBlock: function() {
            return this.element.find(this.options.fullBlockSelector);
        },

        /*
            Стилизация
         */
        _setStyles: function() {
            this.full_block.css({
                overflow: 'hidden'
            });
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
            this.full_block.css({
                overflow: ''
            });
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
            Разворачивание блока
         */
        expand: function($button) {
            if (this._expanded) {
                return
            }

            this._expanded = true;
            this.trigger('before_expand', {
                button: $button
            });

            this.full_block.stop(true, true);

            // рассчет размеров
            var start_height = this.short_block.height();
            this.full_block.removeClass(this.options.hiddenClass);
            var end_height = this.full_block.height();
            this.short_block.addClass(this.options.hiddenClass);

            // анимация
            var that = this;
            this.full_block.height(start_height).animate({
                height: end_height
            }, {
                duration: (Math.abs(end_height - start_height) / 500) * this.options.speed,
                easing: this.options.easing,
                complete: function() {
                    that.full_block.height('');
                    that.trigger('after_expand', {
                        button: $button
                    });
                }
            })
        },

        /*
            Сворачивание блока
         */
        reduce: function($button) {
            if (!this._expanded) {
                return
            }

            this._expanded = false;
            this.trigger('before_reduce', {
                button: $button
            });

            this.full_block.stop(true, true);

            // рассчет размеров
            var start_height = this.full_block.height();
            this.full_block.removeClass(this.options.hiddenClass);
            this.short_block.removeClass(this.options.hiddenClass);
            var end_height = this.short_block.height();
            this.short_block.addClass(this.options.hiddenClass);

            // анимация
            var that = this;
            this.full_block.height(start_height).animate({
                height: end_height
            }, {
                duration: (Math.abs(end_height - start_height) / 500) * this.options.speed,
                easing: this.options.easing,
                complete: function() {
                    that.full_block.height('');
                    that.full_block.addClass(that.options.hiddenClass);
                    that.short_block.removeClass(that.options.hiddenClass);
                    that.trigger('after_reduce', {
                        button: $button
                    });
                }
            })
        }
    });

})(jQuery);
