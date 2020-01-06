(function($) {
    'use strict';

    /*
        https://github.com/vimeo/player.js#create-a-player

        Зависит от:
            jquery-ui.js

        Параметры:
            video       - ключ видео
            autoplay    - автовоспроизведение
            byline      - показывать автора видео
            portrait    - показывать аватар автора
            title       - показывать название видео
            loop        - зациклить видео
            width       - ширина видео
            height      - высота видео

        Пример:
            <div id="player"></div>

            <script>
                $('#player').vimeo({
                    video: 116908919,
                    ended: function(event, data) {
                        console.log('ended:', data)
                    },
                })

                // запуск в режиме паузы на 10-й секунде.
                // TODO: выглядит как гавно, т.к. библиотека Vimeo основана на JS Promise.
                $('.player').vimeo('setPosition', 10).then(function() {
                    $('.player').vimeo('pause');
                });

                // запуск видео
                $('#player').vimeo('play');

                // пауза
                $('#player').vimeo('pause');

                // остановка видео
                $('#player').vimeo('stop');

                // перемотка на позицию в секундах от начала
                $('#player').vimeo('setPosition', 60);

                // громкость на 50%
                $('#player').vimeo('setVolume', 0.5);
            </script>
    */

    var STATE_NONE = 0;
    var STATE_LOADING = 10;
    var STATE_LOADED = 20;
    var state = STATE_NONE;
    var onReady = function(callback, context) {
        var args = Array.prototype.slice.call(arguments, 2);
        var handler = function() {
            return callback.apply(context, args);
        };

        if (state === STATE_LOADED) {
            handler();
        } else {
            $(document).on('vimeo-ready', handler);

            if (state === STATE_NONE) {
                state = STATE_LOADING;
                var script = document.createElement('script');
                script.onload = function() {
                    state = STATE_LOADED;
                    $(document).trigger('vimeo-ready');
                };
                script.src = 'https://player.vimeo.com/api/player.js';
                document.body.appendChild(script);
            }
        }
    };


    var PLACEHOLDER_CLASS = 'vimeo-placeholder';
    $.widget("django.vimeo", {
        options: {
            video: '',

            // опции
            autoplay: false,
            byline: true,
            portrait: true,
            title: true,
            loop: false,
            width: null,
            height: null,

            // события
            loaded: $.noop,
            play: $.noop,
            pause: $.noop,
            ended: $.noop,
            timeupdate: $.noop
        },

        _create: function() {
            var that = this;
            this._promise = new Promise(function(resolve, reject) {
                onReady(function() {
                    that.makeNative();
                    resolve();
                }, this);
            }).catch(function(error) {
                console.error(error);
            });
        },

        _setOptions: function(options) {
            this._super(options);
            if ("video" in options) {
                this.makeNative();
            }
            return this;
        },

        _destroy: function() {
            if (this.player) {
                this.player.unload();
                this.player = null;
                this.element.find('.' + PLACEHOLDER_CLASS).remove();
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
            Создание нативного объекта
         */
        makeNative: function() {
            // хак, т.к. в API нет метода destroy()
            // https://github.com/vimeo/player.js/issues/126
            var $div = $('<div/>').addClass(PLACEHOLDER_CLASS);
            this.element.find('.' + PLACEHOLDER_CLASS).remove();
            this.element.append($div);
            this.player = new Vimeo.Player($div, {
                id: this.options.video,
                autoplay: this.options.autoplay,
                loop: this.options.loop,
                title: this.options.title,
                width: this.options.width,
                height: this.options.height
            });

            // events
            var that = this;
            this.player.on('loaded', function(data) {
                that.trigger('loaded', data);
            });

            this.player.on('play', function(data) {
                that.trigger('play', data);
            });
            this.player.on('pause', function(data) {
                that.trigger('pause', data);
            });
            this.player.on('ended', function(data) {
                that.trigger('ended', data);
            });
            this.player.on('timeupdate', function(data) {
                that.trigger('timeupdate', data);
            });
        },

        play: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.play();
            });
        },

        pause: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.pause();
            });
        },

        stop: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.unload();
            });
        },

        getVolume: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getVolume();
            });
        },

        setVolume: function(value) {
            var that = this;
            return this._promise.then(function() {
                return that.player.setVolume(value);
            });
        },

        getPosition: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getCurrentTime();
            });
        },

        setPosition: function(value) {
            var that = this;
            return this._promise.then($.proxy(function() {
                return that.player.setCurrentTime(value);
            }, that));
        },

        getDuration: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getDuration();
            });
        },

        getPaused: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getPaused();
            });
        },

        getEnded: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getEnded();
            });
        },

        getVideoUrl: function() {
            var that = this;
            return this._promise.then(function() {
                return that.player.getVideoUrl();
            });
        }
    });

})(jQuery);
