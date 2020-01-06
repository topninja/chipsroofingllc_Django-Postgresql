(function($) {

    /*
        Дополнение к Select2, сохраняющее данные AJAX-запроса
        для последующего использования.
     */
    $.extend($.fn.select2.defaults, {
        _cache: {},

        getCacheName: function(query) {
            return query.page + ':' + query.term;
        },

        query: function(query) {
            var cache_name = this.getCacheName(query);
            if (this._cache[cache_name]) {
                query.callback(this._cache[cache_name]);
                return
            }

            // default query function
            var options = this.ajax;
            var url = options.url;
            var transport = $.fn.select2.ajaxDefaults.transport;
            var params = $.extend({}, $.fn.select2.ajaxDefaults.params);
            var data = options.data.call(self, query.term, query.page, query.context);

            if (options.params) {
                if ($.isFunction(options.params)) {
                    $.extend(params, options.params.call(self));
                } else {
                    $.extend(params, options.params);
                }
            }

            var that = this;
            $.extend(params, {
                url: url,
                type: options.type,
                data: data,
                dataType: options.dataType,
                success: function(data) {
                    var results = options.results(data, query.page, query);
                    that._cache[cache_name] = results;
                    query.callback(results);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    var results = {
                        hasError: true,
                        jqXHR: jqXHR,
                        textStatus: textStatus,
                        errorThrown: errorThrown
                    };

                    query.callback(results);
                }
            });
            transport.call(self, params);
        }
    })

})(jQuery);