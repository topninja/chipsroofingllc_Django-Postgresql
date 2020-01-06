(function($) {
    'use strict';

    /*
        Кастомное поле ввода чисел, которое подключется к обёртке над
        стандартным полем input[type="number"]

        Зависит от:
            jquery.utils.js

        Параметры:
            buttonClass      - класс, добавляемый кнопкам
            inputClass       - класс, добавляемый полю
            min              - минимальное значение поля (перезапишет аттрибут)
            max              - максимальное значение поля (перезапишет аттрибут)

        События:
            // Перед изменение значения. Если вернет false - значение не изменится.
            before_change(new_value, old_value)

            // После изменения значения
            after_change(new_value, old_value)

        Пример:
            <div class="custom-counter">
                <input type="number" value="1">
            </div>

            $('.custom-counter').each(function() {
                CustomCounter(this);
            });
    */

    window.CustomCounter = Class(EventedObject, function CustomCounter(cls, superclass) {
        cls.defaults = {
            wrapperClass: 'custom-counter-wrapper',
            buttonClass: 'custom-counter-button',
            inputClass: 'custom-counter-input',

            min: '',
            max: '',
            step: 1
        };

        cls.DATA_KEY = 'counter';


        cls.init = function(root, options) {
            superclass.init.call(this);

            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // поле
            this.$input = this.$root.find('input').first();
            if (!this.$input.length) {
                return this.raise('input element not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$input.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // создаем кнопки и обертку
            this.$wrapper = $('<div>').addClass(this.opts.wrapperClass);
            this.$wrapper.prependTo(this.$root).append(this.$input);
            this.$decrBtn = $('<div>').insertBefore(this.$input);
            this.$incrBtn = $('<div>').insertAfter(this.$input);

            // вешаем классы
            this.$input.addClass(this.opts.inputClass);
            this.$decrBtn.addClass(this.opts.buttonClass + ' decr');
            this.$incrBtn.addClass(this.opts.buttonClass + ' incr');

            // границы значений
            this.min = $.isNumeric(this.opts.min) ? this.opts.min : this.$input.prop('min');
            this.max = $.isNumeric(this.opts.max) ? this.opts.max : this.$input.prop('max');
            this.step = $.isNumeric(this.opts.step) ? this.opts.step : this.$input.prop('step');
            if (this.$input.prop('type') === 'number') {
                if (this.min) {
                    this.$input.prop('min', this.min);
                }
                if (this.min) {
                    this.$input.prop('max', this.max);
                }
                if (this.step) {
                    this.$input.prop('step', this.step);
                }
            }

            // форматируем текущее значение
            this._format();

            // уменьшение значения
            var that = this;
            this.$decrBtn.on('click.counter', function() {
                that.decrement();
                return false;
            });

            // увеличение значения
            this.$incrBtn.on('click.counter', function() {
                that.increment();
                return false;
            });


            this.$input.on('input.counter', function() {
                // форматирование значения при потере фокуса
                that._format();
            }).on('keypress.counter', function(e) {
                // форматирование значения при нажатии Enter
                if (e.which === 13) {
                    that._format();
                }
            }).on('mousewheel.counter', function(e) {
                // Прокрутка колеса на поле изменяет его значение
                if (e.deltaY < 0) {
                    that.decrement();
                } else {
                    that.increment();
                }

                return false
            });

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$decrBtn.remove();
            this.$incrBtn.remove();
            this.$input.removeClass(this.opts.inputClass);
            this.$input.prependTo(this.$root);
            this.$input.off('.counter');
            this.$wrapper.remove();
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        /*
            Форматирование значения
         */
        cls._formatted = function(value) {
            value = parseInt(value);
            if (isNaN(value)) {
                return value;
            }

            if ($.isNumeric(this.min)) {
                value = Math.max(value, this.min);
            }

            if ($.isNumeric(this.max)) {
                value = Math.min(value, this.max);
            }

            return value
        };

        /*
            Форматирование текущего значения input
         */
        cls._format = function() {
            var value = this._formatted(this.$input.val());
            if (isNaN(value)) {
                this.$input.val('');
            } else {
                this.$input.val(value);
            }
        };

        /*
            Получение и установка значения
         */
        cls.value = function(value) {
            var current = this._formatted(this.$input.val());
            if (value === undefined) {
                // получение значения
                return current;
            }

            value = this._formatted(value);
            if ((value === current) || (isNaN(value) && isNaN(current))) {
                return this;
            }

            if (this.trigger('before_change', value, current) === false) {
                return this;
            }
            this.$input.val(value);
            this.trigger('after_change', value, current);
            return this;
        };

        /*
            Инкремент значения
         */
        cls.increment = function() {
            var result;
            var current = this._formatted(this.$input.val());
            if (isNaN(current)) {
                result = this.min || this.step;
            } else {
                result = current + this.step;
            }

            this.value(result);
            this.$input.trigger('change');
            return this;
        };

        /*
            Декремент значения
         */
        cls.decrement = function() {
            var result;
            var current = this._formatted(this.$input.val());
            if (isNaN(current)) {
                result = this.max || -this.step;
            } else {
                result = current - this.step;
            }

            this.value(result);
            this.$input.trigger('change');
            return this;
        };
    });

})(jQuery);
