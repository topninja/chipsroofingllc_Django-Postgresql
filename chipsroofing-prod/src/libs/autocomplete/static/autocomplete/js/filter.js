(function($) {
    'use strict';

    var event_ns = 1;
    window.AutocompleteFilter = Class(Object, function AutocompleteFilter(cls, superclass) {
        cls.defaults = {
            url: '',
            multiple: false,
            expression: 'title__icontains',
            minimum_input_length: 2
        };

        cls.DATA_KEY = 'autocomplete_filter';

        cls.init = function(element, options) {
            this.$elem = $(element).first();
            if (!this.$elem.length) {
                return this.raise('element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            if (!this.opts.url) {
                return this.raise('url required');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$elem.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            this.name = this.$elem.data('name');

            // Поля, от которых зависит текущее поле
            var $search_form = $('#changelist-search');
            var filters = this.$elem.data('filters').split(',');
            filters = filters.map(function(item) {
                return $search_form.find('[data-name="' + item + '"]').get(0);
            });
            this.$filters = $(filters.filter(Boolean));

            // при изменении зависимости вызываем событие изменения на текущем элементе
            var that = this;
            this.event_ns = event_ns++;
            this.$filters.on('change.autocomplete_filter' + this.event_ns, function() {
                that.$elem.select2('data', null);
            });

            // инициализация select2
            this.initSelect2();

            this.$elem.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$filters.off('.autocomplete_filter' + this.event_ns);
            this.$elem.removeData(this.DATA_KEY);
            this.$elem.select2('destroy');
        };

        /*
            Возвращает значения, от которых зависит текущее поле
         */
        cls._parentValues = function() {
            return Array.prototype.map.call(this.$filters, function(item) {
                return $(item).val()
            }).join(';');
        };

        /*
            Инициализация Select2
         */
        cls.initSelect2 = function() {
            var that = this;
            this.$elem.select2({
                allowClear: true,
                multiple: this.opts.multiple,
                minimumInputLength: this.opts.minimum_input_length,
                getCacheName: function(query) {
                    return query.page + ':' + query.term + ':' + that.name + ':' + that._parentValues();
                },
                ajax: {
                    url: this.opts.url,
                    type: 'POST',
                    quietMillis: 1,
                    dataType: 'json',
                    data: function(term, page, page_limit) {
                        return {
                            q: term,
                            page_limit: page_limit || 30,
                            page: page,
                            values: that._parentValues(),
                            expression: that.opts.expression
                        };
                    },
                    results: function(data, page) {
                        return {
                            results: data.result,
                            more: (page * 30) < data.total
                        };
                    }
                },
                initSelection: function(element, callback) {
                    var id = that.$elem.val();
                    if (!id) {
                        return
                    }

                    $.ajax(that.opts.url, {
                        type: 'POST',
                        dataType: "json",
                        data: {
                            q: id,
                            values: that._parentValues(),
                            expression: 'pk__in'
                        },
                        success: function(response) {
                            if (that.opts.multiple) {
                                response = response.result;
                            } else {
                                response = response.result.shift();
                            }
                            that.$elem.select2("data", response);
                            callback(response);
                        }
                    });
                },
                escapeMarkup: function(m) {
                    return m;
                }
            });
        };
    });


    $(document).ready(function() {
        $('.autocomplete-filter').each(function() {
            var $input = $(this);
            var input_data = $input.data();

            window.AutocompleteFilter($input, {
                url: input_data.url,
                multiple: Boolean(parseInt(input_data.multiple)),
                expression: input_data.expression,
                minimum_input_length: input_data.minimum_input_length
            });
        })
    });

})(jQuery);