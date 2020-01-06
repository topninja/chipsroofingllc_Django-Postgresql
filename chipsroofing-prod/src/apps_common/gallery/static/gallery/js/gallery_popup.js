(function($) {
    'use strict';

    /*
        Стандартная галерея, показывающая фото и видео на весь экран
        в модальном окне.

        Требует:
            jquery.utils.js,
            jquery.popups.js,
            slider.js,
            jquery.youtube.js,
            jquery.vimeo.js

        Параметры:
            previews: str / jquery       - превью-элементы галереи, содержащие код для окна
            activePreview: DOM / index   - DOM-элемент или индекс активного превью-элемента
            keyboard: true / false       - прокручивать галерею стрелками (плохо для видео)
            keyboardAnimation: str       - имя анимации при нажатии стрелок


        Внутри каждого превью должен быть тэг <script>, содержащий HTML-код,
        содержимое которого будет элементом слайдера. Поэтому, в содержимом
        <script> должен быть ровно ОДИН корневой элемент.

        Для видео-элемента обязательно наличие аттрибутов data-provider и data-key
        у родительского элемента, расположенного в <script>.

        Пример HTML:
            <div id="gallery">
              <div class="item">
                <img src="...">

                <!-- popup content -->
                <script type="text/template">
                  <div class="image-item">
                    <img src="...">
                  </div>
                </script>
            </div>

            <div class="item">
              <img src="...">

              <!-- popup content -->
              <script type="text/template">
                <div class="video-item" data-provider="youtube" data-key="...">
                  <img src="...">
                  <div class="play-btn"></div>
                </div>
              </script>
            </div>

            $('#gallery').find('.item').on('click', function() {
                $.gallery({
                    previews: '#gallery .item',
                    activePreview: this
                });
            });

     */



    window.GalleryPopup = Class(OverlayedPopup, function GalleryPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            classes: 'gallery-popup',
            hideOnClick: false,

            videoLoadingClass: 'loading',
            videoPlayingClass: 'playing',

            previews: '',
            activePreview: 0,
            keyboard: false,
            keyboardAnimation: 'side'
        });

        cls.OVERLAY_ID = 'gallery-popup-overlay';
        cls.CONTAINER_ID = 'gallery-popup-container';
        cls.YOUTUBE_VIDEO = 'youtube';
        cls.VIMEO_VIDEO = 'vimeo';

        cls.init = function(options) {
            superclass.init.call(this, options);

            this.$previews = this.opts.previews;
            if (!this.$previews) {
                return this.raise('previews required');
            }
            if (typeof this.$previews === 'string') {
                // получаем jquery, в случае селектора
                this.$previews = $(this.$previews);
            }
            if (!this.$previews.jquery || !this.$previews.length) {
                return this.raise('previews not found');
            }
        };

        /*
            Создание элемента окна галереи из элемента превью
         */
        cls._buildItem = function($preview) {
            var $template = $preview.find('script[type="text/template"]').first();
            if ($template.length) {
                return $($template.html());
            }
        };

        /*
            Инициализация элемента-картинки
         */
        cls._initImageItem = function($item, item_data) {

        };

        /*
            Инициализация элемента-видео
         */
        cls._initVideoItem = function($item, item_data) {
            var that = this;
            var $playBtn = $item.find('.play-btn');
            $playBtn.on('click', function() {
                that.playVideo($item);
            });
        };

        /*
            Установка содержимого окна
         */
        cls.resetContent = function() {
            var that = this;
            var $items = this.$previews.map(function(i, preview) {
                var $preview = $(preview);

                var $item = that._buildItem($preview);
                if (!$item || !$item.length) {
                    that.warn('not builded item from preview ', $preview);
                    return;
                }

                if ($item.length > 1) {
                    that.warn('item contains more that one element ', $preview);
                    return;
                }

                // Инициализация
                var item_data = $item.data();
                if (item_data.provider && item_data.key) {
                    that._initVideoItem($item, item_data);
                } else {
                    that._initImageItem($item, item_data);
                }

                return $item.get(0);
            });

            // хоть один элемент галереи должен быть
            if (!$items.length) {
                return this.raise('at least one gallery item required');
            }

            // слайдер
            var $slider = $('<div>').addClass('slider no-slider').append(
                $items.addClass('slider-item')
            );

            this.$content.html($slider);
        };

        /*
            Создание объекта слайдера
         */
        cls.makeSlider = function() {
            return Slider(this.$content.find('.slider'), {
                sliderHeight: Slider.prototype.HEIGHT_NONE
            }).attachPlugins([
                SliderSideAnimation({}),
                SliderSideShortestAnimation({}),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    slideMarginPercent: 2
                })
            ])
        };

        /*
            Добавление слайдера
         */
        cls.extraDOM = function() {
            superclass.extraDOM.call(this);

            this.slider = this.makeSlider();
            if (!this.slider) {
                this.error('slider wasn\'t created');
                return;
            }

            // выделение выбранного слайда
            var preview;
            var active_index = 0;
            if (this.opts.activePreview.jquery) {
                // jQuery-селектор с превью-элементом
                preview = this.opts.activePreview.get(0);
                active_index = this.$previews.toArray().indexOf(preview);
            } else if (this.opts.activePreview.nodeType === 1) {
                // DOM-элемент превью-элемента
                preview = this.opts.activePreview;
                active_index = this.$previews.toArray().indexOf(preview);
            } else {
                // индекс активного слайда
                active_index = this.opts.activePreview;
            }

            // проверка индекса
            if ((active_index < 0) || (active_index >= this.slider.$slides.length)) {
                active_index = 0;
                this.warn('active preview not found', this.opts.activePreview);
            }

            var $activeSlide = this.slider.$slides.eq(active_index);
            this.slider.slideTo($activeSlide, 'instant');

            // нажатие стрелок на клавиатуре
            if (this.opts.keyboard) {
                var that = this;
                $(document).on('keydown.popup', function(event) {
                    if (event.which === 39) {
                        that.slider.slideNext(that.opts.keyboardAnimation);
                    } else if (event.which === 37) {
                        that.slider.slidePrevious(that.opts.keyboardAnimation);
                    }
                });
            }
        };

        /*
            Уничтожение слайдера
         */
        cls._removeDOM = function() {
            if (this.slider) {
                this.slider.destroy();
                this.slider = null;
            }
            superclass._removeDOM.call(this);
        };

        /*
            Инициализация видеоплеера
         */
        cls.playVideo = function($item) {
            /** @namespace item_data.provider */

            var item_data = $item.data();
            if (item_data.provider === this.YOUTUBE_VIDEO) {
                this._playYoutube($item, item_data);
            } else if (item_data.provider === this.VIMEO_VIDEO) {
                this._playVimeo($item, item_data);
            } else {
                this.warn('undefined video provider:', item_data.provider);
                return
            }

            // остановка видео при переходе на другой слайд и закрытии окна
            var that = this;
            this.on('before_hide.video', function() {
                that.stopVideo($item);
            });

            if (this.slider) {
                this.slider.on('changeSlide.video', function() {
                    that.stopVideo($item);
                });
            }
        };

        cls._playYoutube = function($item, item_data) {
            var that = this;
            $item.addClass(this.opts.videoLoadingClass).youtube({
                video: item_data.key,
                autoplay: true,
                loaded: function() {
                    $item.removeClass(that.opts.videoLoadingClass);
                    $item.addClass(that.opts.videoPlayingClass);
                }
            })
        };

        cls._playVimeo = function($item, item_data) {
            var that = this;
            $item.addClass(this.opts.videoLoadingClass).vimeo({
                video: item_data.key,
                autoplay: true,
                loaded: function() {
                    $item.removeClass(that.opts.videoLoadingClass);
                    $item.addClass(that.opts.videoPlayingClass);
                }
            })
        };

        /*
            Уничтожение видеоплеера
         */
        cls.stopVideo = function($item) {
            var item_data = $item.data();
            if (item_data.provider === this.YOUTUBE_VIDEO) {
                $item.youtube('destroy');
            } else if (item_data.provider === this.VIMEO_VIDEO) {
                $item.vimeo('destroy');
            } else {
                this.warn('undefined video provider:', item_data.provider);
                return
            }

            $item.removeClass(this.opts.videoLoadingClass);
            $item.removeClass(this.opts.videoPlayingClass);

            this.off('.video');
            if (this.slider) {
                this.slider.off('.video');
            }
        };
    });

    $.gallery = function(options) {
        var popup = window.GalleryPopup(options);
        return popup && popup.show();
    };

})(jQuery);