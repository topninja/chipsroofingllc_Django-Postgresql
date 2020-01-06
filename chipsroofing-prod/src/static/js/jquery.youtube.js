(function($) {
    'use strict';

    /*
        https://developers.google.com/youtube/iframe_api_reference?hl=ru

        Зависит от:
            jquery-ui.js

        Параметры:
            video       - строка с ключем видео
            autoplay    - автовоспроизведение
            controls    - кнопки управления (0 - нету, 1/2 - есть)
            fullscreen  - показывать кнопку "развернуть на весь экран"
            loop        - зациклить видео
            playlist    - воспроизводить плейлист после заданного видео
            rel         - предлагать похожие видео
            showinfo    - показывать информацию о видео

        Пример:
            <div id="player"></div>

            <script>
                $('#player').youtube({
                    video: 'M7lc1UVf-VE'
                })

                // запуск видео
                $('#player').youtube('play');

                // пауза
                $('#player').youtube('pause');

                // остановка видео
                $('#player').youtube('stop');

                // перемотка на позицию в секундах от начала
                $('#player').youtube('setPosition', 60);

                // громкость на 50%
                $('#player').youtube('setVolume', 0.5);
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
            $(document).on('youtube-ready', handler);

            if (state === STATE_NONE) {
                state = STATE_LOADING;
                var script = document.createElement('script');
                window.onYouTubeIframeAPIReady = function() {
                    state = STATE_LOADED;
                    $(document).trigger('youtube-ready');
                };
                script.src = 'https://www.youtube.com/iframe_api';
                document.body.appendChild(script);
            }
        }
    };


    var CHECK_POSITION_TIMEOUT = 100;
    var PLACEHOLDER_CLASS = 'youtube-placeholder';

    $.widget("django.youtube", {
        options: {
            video: '',

            // опции
            autoplay: false,
            controls: 2,
            fullscreen: true,
            loop: false,
            playlist: null,
            rel: false,
            showinfo: true,

            // события
            loaded: $.noop,
            play: $.noop,
            pause: $.noop,
            ended: $.noop,
            timeupdate: $.noop
        },

        _create: function() {
            var that = this;
            onReady(function() {
                that.makeNative();
            }, this);
        },

        _setOptions: function(options) {
            this._super(options);
            if ("video" in options) {
                this.stop();
                this.makeNative();
            }
            return this;
        },

        _destroy: function() {
            this._stopInterval();
            if (this.player) {
                this.player.destroy();
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
            /** @namespace YT.Player */
            var that = this;
            var $div = $('<div/>').addClass(PLACEHOLDER_CLASS);
            this.element.find('.' + PLACEHOLDER_CLASS).remove();
            if (this.iframe) {
                this.iframe.remove();
                this.iframe = null;
            }
            this.element.append($div);

            this.player = new YT.Player($div.get(0), {
                videoId: this.options.video,
                playerVars: {
                    autoplay: Number(Boolean(this.options.autoplay)),
                    controls: Number(this.options.controls),
                    fs: Number(Boolean(this.options.fullscreen)),
                    loop: Number(Boolean(this.options.loop)),
                    playlist: this.options.playlist,
                    rel: Number(Boolean(this.options.rel)),
                    showinfo: Number(Boolean(this.options.showinfo)),
                    hl: document.documentElement.getAttribute('lang') || 'en'
                },
                events: {
                    onReady: function(event) {
                        /** @namespace event.target.getIframe */
                        that.iframe = $(event.target.getIframe());
                        that.trigger('loaded', event);
                    },
                    onStateChange: function(event) {
                        /** @namespace YT.PlayerState.UNSTARTED */
                        /** @namespace YT.PlayerState.BUFFERING */
                        /** @namespace YT.PlayerState.PLAYING */
                        /** @namespace YT.PlayerState.PAUSED */
                        /** @namespace YT.PlayerState.ENDED */
                        var code = event.data;
                        if (code === YT.PlayerState.UNSTARTED) {
                            that._stopInterval();
                        } else if (code === YT.PlayerState.BUFFERING) {

                        } else if (code === YT.PlayerState.PLAYING) {
                            that._startInterval();
                            that.trigger('play');
                        } else if (code === YT.PlayerState.PAUSED) {
                            that._stopInterval();
                            that.trigger('pause');
                        } else if (code === YT.PlayerState.ENDED) {
                            that._stopInterval();
                            that.trigger('pause');
                            that.trigger('ended');
                        }
                    }
                }
            });
        },

        /*
            Создание таймера, проверяющего позицию видео
         */
        _startInterval: function() {
            this._stopInterval();
            this._currentPosition = -1;
            this._timer = setInterval($.proxy(this._updateTime, this), CHECK_POSITION_TIMEOUT);
        },

        /*
            Остановка таймера, проверяющего позицию видео
         */
        _stopInterval: function() {
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        },

        _updateTime: function() {
            var position = this.getPosition() || 0;
            if (position !== this._currentPosition) {
                this._currentPosition = position;
                var duration = this.getDuration();
                this.trigger('timeupdate', {
                    seconds: parseFloat(position.toFixed(3)),
                    percent: parseFloat((position / duration).toFixed(3)),
                    duration: duration
                });
            }
        },

        play: function() {
            this.player.playVideo();
        },

        pause: function() {
            this.player.pauseVideo();
        },

        stop: function() {
            this.player.stopVideo();
        },

        getVolume: function() {
            var volume = this.player.getVolume();
            return volume / 100;
        },

        setVolume: function(value) {
            this.player.setVolume(value / 100);
        },

        getPosition: function() {
            return this.player.getCurrentTime();
        },

        setPosition: function(value) {
            this.player.seekTo(value);
        },

        getDuration: function() {
            return this.player.getDuration();
        },

        nextVideo: function() {
            this.player.nextVideo();
        },

        previousVideo: function() {
            this.player.previousVideo();
        },

        getPaused: function() {
            return [-1, 0, 2, 5].indexOf(this.player.getPlayerState()) >= 0;
        },

        getEnded: function() {
            return this.player.getPlayerState() === 0;
        },

        getVideoUrl: function() {
            return this.player.getVideoUrl();
        }
    });










    window.YouTube = Class(EventedObject, function YouTube(cls, superclass) {
        cls.defaults = {
            video: ''
        };

        // интервал проверки времени воспроизведения
        cls.CHECK_POSITION_TIMEOUT = 100;


        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.stop();
            if (this.native) {
                this.native.destroy();
                this.$iframe = null;
                this.native = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Получение ссылки на видео
         */
        cls.getVideoUrl = function() {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            return this.native.getVideoUrl();
        };

        /*
            Загрузка другого видео по его идентификатору
         */
        cls.loadVideo = function(videoId) {
            if (!this.native) {
                this.warn('not ready yet');
                return this;
            }

            this.stopInteraval();
            this.trigger('pause');

            this.native.loadVideoById(videoId);
            return this;
        };
    });

})(jQuery);
