(function($) {
    'use strict';

    // собираем все ID при инициализации в один объект,
    // чтобы запросить их одним махом.
    var mass_requests = {};

    var formatSelection = function(state) {
        if (!state.id) {
            return state.text;
        }
        return state.selected_text || state.text;
    };

    var event_ns = 1;
    window.Autocomplete = Class(Object, function Autocomplete(cls, superclass) {
        cls.defaults = {
            url: '',
            min_chars: 2,
            filters: [],
            expressions: 'title__icontains',
            multiple: false
        };

        cls.DATA_KEY = 'autocomplete';


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

            // имя элемента
            this.name = this.$elem.attr('name');
            if (!this.name) {
                return this.raise('element name attribute not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$elem.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // Поля, от которых зависит текущее поле
            var filters = this.opts.filters;
            if (typeof filters === 'string') {
                filters = filters.split(',');
            } else {
                filters = filters.concat();
            }

            if (this.name.indexOf('-') >= 0) {
                var formset_prefix = this.name.split('-').slice(0, -1).join('-');
                filters = filters.map(function(item) {
                    return document.getElementById('id_' + item.replace('__prefix__', formset_prefix));
                })
            } else {
                filters = filters.map(function(item) {
                    return document.getElementById('id_' + item);
                })
            }
            this.$filters = $(filters.filter(Boolean));

            // при изменении зависимости вызываем событие изменения на текущем элементе
            var that = this;
            this.event_ns = event_ns++;
            this.$filters.on('change.autocomplete' + this.event_ns, function() {
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
            this.$filters.off('.autocomplete' + this.event_ns);
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
                minimumInputLength: this.opts.min_chars,
                formatSelection: formatSelection,
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
                            expressions: that.opts.expressions
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

                    var key = that.opts.url;
                    var record = {
                        id: id,
                        object: that,
                        callback: callback,
                        filters: that.$filters.length
                    };

                    if (key in mass_requests) {
                        mass_requests[key].push(record);
                    } else {
                        mass_requests[key] = [record];
                    }
                },
                escapeMarkup: function(m) {
                    return m;
                }
            });
        };
    });


    $(document).ready(function() {
        $('.autocomplete_widget').each(function() {
            var $this = $(this);
            if (!$this.closest('.empty-form').length) {
                window.Autocomplete(this, $this.data());
            }
        });

        // Запрос собранных данных
        $.each(mass_requests, function(url, records) {
            var with_filters = [];
            var without_filters = [];

            // распределение зависимых и независимых объектов
            records.forEach(function(record) {
                if (record.filters) {
                    with_filters.push(record);
                } else {
                    without_filters.push(record);
                }
            });

            // запрос независимых объектов
            if (without_filters.length) {
                var ids = $.unique(without_filters.map(function(record) {
                    return record.id
                }));

                $.ajax(url, {
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: ids.join(','),
                        expressions: 'pk__in'
                    },
                    success: function(response) {
                        var data;
                        var result = response.result;
                        if (!result || !result.length) {
                            return
                        }

                        // формирование словаря из результатов
                        var result_dict = {};
                        $.each(result, function(i, item) {
                            result_dict[item.id] = item.text;
                        });

                        // обработка каждого поля
                        $.each(without_filters, function(i, record) {
                            if (!record.object.opts.multiple) {
                                data = {
                                    id: record.id,
                                    text: result_dict[record.id]
                                };
                            } else {
                                data = record.id.split(',').map($.trim).filter(Boolean).map(function(pk) {
                                    return {
                                        id: pk,
                                        text: result_dict[pk]
                                    }
                                });
                            }

                            record.object.$elem.select2("data", data);
                            record.callback(data);
                        });
                    },
                    error: $.parseError()
                });
            }

            // запрос зависимых объектов
            with_filters.forEach(function(record) {
                $.ajax(url, {
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: record.id,
                        values: record.object._parentValues(),
                        expressions: 'pk__in'
                    },
                    success: function(response) {
                        var result = response.result;
                        if (!result || !result.length) {
                            return
                        }

                        if (!record.object.opts.multiple) {
                            result = result[0];
                        }

                        record.object.$elem.select2("data", result);
                        record.callback(result);
                    },
                    error: $.parseError()
                });
            });
        });
        mass_requests = {};

        if ($.attachRelatedWidgetSupport) {
            $.attachRelatedWidgetSupport('.autocomplete_widget');
        }

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_widget', function(inline_prefix, row) {
                row.find('.autocomplete_widget').each(function() {
                    window.Autocomplete(this, $(this).data());
                });
            });
        }
    });

    // фикс для джанговских кнопок добавления / редактирования ForeignKey
    $(document).on('add-related', 'input.autocomplete_widget', function(event, id, text) {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            var item = {
                id: id,
                text: text
            };

            if (select2_object.opts.multiple) {
                var data = select2_object.data();
                data.push(item);
                select2_object.data(data);
            } else {
                select2_object.data(item);
            }
        }
    }).on('change-related', 'input.autocomplete_widget', function(event, objId, text, id) {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            var item = {
                id: id,
                text: text
            };

            select2_object.data(item);
        }
    }).on('delete-related', 'input.autocomplete_widget', function(event, objId) {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            select2_object.data(null);
        }
    });

})(jQuery);
