(function($) {
    'use strict';

    window.InstagramWidget = Class(EventedObject, function InstagramWidget(cls, superclass) {
        cls.DATA_KEY = 'instagram';

        cls.defaults = {
            token: '',
            user_id: '',
            tag: '',
            limit: 0
        };

        cls.init = function(element, options) {
            superclass.init.call(this);

            this.$root = $(element).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);
            if (!this.opts.token) {
                return this.raise('"access_token" undefined');
            }
            if (!this.opts.user_id && !this.opts.tag) {
                return this.raise('one of ["user_id", "tag"] should be defined');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // запрос данных с Instagram
            if (this.opts.tag) {
                this.fetchData(this.tagMediaURL());
            } else {
                this.fetchData(this.userMediaURL());
            }

            this.$root.data(this.DATA_KEY, this);
        };

        cls.destroy = function() {
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        cls.userMediaURL = function() {
            return 'https://api.instagram.com/v1/users/' + this.opts.user_id + '/media/recent/';
        };

        cls.tagMediaURL = function() {
            return 'https://api.instagram.com/v1/tags/' + this.opts.tag + '/media/recent/';
        };

        cls.fetchData = function(url) {
            var that = this;
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'jsonp',
                data: {
                    access_token: this.opts.token,
                    count: this.opts.limit
                },
                success: function(data) {
                    /** @namespace data.meta.error_message */

                    if (parseInt(data.meta.code) !== 200) {
                        that.error(data.meta.error_message + ' (code ' + data.meta.code + ')');
                        that.trigger('error', data);
                    } else {
                        that.trigger('success', data);
                    }
                },
                error: function(xhr, status) {
                    /** @namespace xhr.status_text */

                    that.error(xhr.status_text + ' (code ' + status + ')');
                    that.trigger('error', data);
                }
            });
        };
    });


    $(document).ready(function() {
        $('.instagram-widget').each(function() {
            var $elem = $(this);
            var elem_data = $elem.data();

            window.InstagramWidget($elem, {
                token: elem_data.access_token,
                user_id: elem_data.user_id || 'self',
                tag: elem_data.tag || '',
                limit: elem_data.limit
            }).on('success', function(response) {
                response.data.forEach(function(obj) {
                    /** @namespace obj.images.low_resolution.url */

                    $elem.append(
                        $('<img>').attr({
                            src: obj.images.low_resolution.url,
                            width: 320,
                            height: 320
                        })
                    );
                })
            }).on('error', function() {
                $elem.remove();
            });
        })
    });

})(jQuery);