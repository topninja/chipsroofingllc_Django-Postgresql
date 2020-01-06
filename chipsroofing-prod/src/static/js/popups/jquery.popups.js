(function($) {
    'use strict';

    /*
        Плагин модальных окон.

        В один момент времени может существовать множество окон,
        но видимо всегда только одно окно.
        Текущее видимое окно можно получить через getCurrentPopup();

        Любые элементы с классом Popup.CLOSE_BUTTON_CLASS при клике будут закрывать окно.

        После скрытия окна, оно удаляется из DOM.

        Высота окна динамическая и зависит от содержимого.

        Параметры:
            // Классы контейнера окна и оверлея
            classes: ''

            // Классы, добавляемые к <body>, когда окно открыто
            body_classes: ''

            // HTML или метод, возвращающий содержимое окна
            content: ''

            // Скорость анимации показа и скрытия окна
            speed: 400

        Методы объекта окна:
            // Показ окна. Возвращает Deferred-объект
            popup.show()

            // Скрытие окна. Возвращает Deferred-объект
            popup.hide()

            // Мгновенное уничтожение окна
            popup.destroy()

        События:
            // Окно создано и готово к показу (метод show() уже вызван)
            ready

            // Перед показом окна. Если вернет false - показ будет отменен.
            before_show

            // После завершения анимации показа
            after_show

            // Перед скрытием окна. Если вернет false - скрытие будет отменено.
            before_hide

            // После завершения анимации скрытия.
            after_hide

        Примеры:
            // Мгновенное уничтожение окна, открытого в данный момент
            var current_popup = getCurrentPopup();
            if (current_popup) {
                current_popup.destroy()
            }

            // Создание скрытого окна с оверлеем
            var popup = OverlayedPopup({
                classes: 'my-popup',
                content: '<h1 class="title-h1">Hello</h1>'
            });

            // Создание и показ окна с оверлеем через jQuery-алиас
            $.popup({
                classes: 'my-popup',
                content: '<h1 class="title-h1">Overlayed popup</h1>'
            }).show()

            // Динамическое содержимое окна
            $.popup({
                classes: 'my-popup',
            }).on('ready', function() {
                this.$content.prepend('<h1>Hello</h1>');
            }).show()

            // Показ окна с выводом сообщения после окончания анимации
            popup.on('after_show', function() {
                console.log('Окно показано')
            }).show();

            // Скрытие окна и уничтожение после завершения анимации
            popup.on('after_hide', function() {
                console.log('Окно скрыто');
            }).hide();

        Инфа для разработчика:
            Блок $content введен в $window из-за необходимости разных значений overflow.
    */

    /** @namespace $body.scrollTop */

    // определение ширины скроллбара
    var scrollWidth = (function() {
        var div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.overflowY = 'scroll';
        div.style.width = '20px';
        div.style.visibility = 'hidden';
        div.style.padding = '0';
        div.style.fontSize = '0';
        div.style.borderWidth = '0';
        document.body.appendChild(div);
        var result = div.offsetWidth - div.clientWidth;
        document.body.removeChild(div);
        return result;
    })();

    // jQuery body
    var $body = $(document.body);

    // текущее окно
    var currentPopup = null;
    var isIPhone = navigator.userAgent.match(/(iPhone|iPod|iPad)/i);

    /*
        Получение текущего окна
     */
    window.getCurrentPopup = function() {
        return currentPopup;
    };

    window.Popup = Class(EventedObject, function Popup(cls, superclass) {
        cls.defaults = {
            classes: '',
            body_classes: '',
            content: '',
            speed: 200,
            easingShow: 'linear',
            easingHide: 'linear'
        };

        cls.CONTAINER_ID = 'popup-container';
        cls.WRAPPER_CLASS = 'popup-wrapper';
        cls.WINDOW_CLASS = 'popup-window';
        cls.CONTENT_CLASS = 'popup-content';
        cls.CLOSE_BUTTON_CLASS = 'close-popup';

        // класс <body>, вешающийся при показе окна
        cls.BODY_OPENED_CLASS = 'popup-opened';


        cls.init = function(options) {
            superclass.init.call(this);

            // настройки
            this.opts = $.extend(true, {}, this.defaults, options);

            this._opened = false;
            this._visible = false;
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this._beforeHide();
            this._showScrollbar();
            this._afterHide();
            superclass.destroy.call(this);
        };

        /*
            Создание DOM
         */
        cls._createDOM = function() {
            // Создание DOM (изначально скрытого)
            this.$container = $('<div>').attr('id', this.CONTAINER_ID).hide();
            this.$windowWrapper = $('<div>').addClass(this.WRAPPER_CLASS);
            this.$window = $('<div>').addClass(this.WINDOW_CLASS);
            this.$content = $('<div>').addClass(this.CONTENT_CLASS);

            this.$window.append(this.$content);
            this.$windowWrapper.append(this.$window);
            this.$container.append(this.$windowWrapper);
            $body.append(this.$container);

            // classes
            this.$container.addClass('popup ' + this.opts.classes);

            // content
            this.resetContent();

            // дополнительные элементы
            this.extraDOM();

            this.trigger('ready');
        };

        /*
            Удаление DOM
         */
        cls._removeDOM = function() {
            $('#' + this.CONTAINER_ID).remove();
        };

        /*
            Установка содержимого $content
         */
        cls.resetContent = function() {
            var content;
            if ($.isFunction(this.opts.content)) {
                content = this.opts.content.call(this);
            } else {
                content = this.opts.content;
            }

            if (content) {
                this.$content.empty();
                this.$content.html(content);
            }
        };

        /*
            Добавление в окно дополнительных элементов / обработчиков событий
         */
        cls.extraDOM = function() {

        };

        //=======================
        // Скроллбар <body>
        //=======================

        // Есть ли дефолтный скроллбар
        cls._hasScrollBar = function() {
            return document.body.scrollHeight > document.body.clientHeight;
        };

        // Скрытие дефолтного скроллбара
        cls._hideScrollbar = function() {
            var body_data = $body.data();
            var body_padding = parseInt($body.css('paddingRight')) || 0;
            body_data._popup_padding = body_padding;

            if (isIPhone) {
                // fix: на iOs не пропадает скролл
                body_data._popup_scroll = $body.scrollTop();
                $('#wrapper').css({
                    position: 'fixed',
                    transform: 'translateY(' + (-body_data._popup_scroll) + 'px)'
                })
            }

            $body.addClass(this.BODY_OPENED_CLASS);


            if (this._hasScrollBar()) {
                $body.css({
                    paddingRight: body_padding + scrollWidth
                });
            }
        };

        // Показ дефолтного скроллбара
        cls._showScrollbar = function() {
            var body_data = $body.data();
            if (body_data._popup_padding !== undefined) {
                var body_padding = parseInt(body_data._popup_padding) || 0;

                $body.css({
                    paddingRight: body_padding
                });
            }

            $body.removeClass(this.BODY_OPENED_CLASS);

            if (isIPhone) {
                // fix: на iOs не пропадает скролл
                $('#wrapper').css({
                    position: '',
                    transform: ''
                });
                $body.scrollTop(body_data._popup_scroll || 0);
            }

            $body.removeData('_popup_padding _popup_scroll');
        };

        //=======================
        // Методы
        //=======================

        /*
            Открыто ли окно (true до анимации)
         */
        cls.is_opened = function() {
            return this._opened;
        };

        /*
            Видимо ли окно (true после анимации)
         */
        cls.is_visible = function() {
            return this._visible;
        };

        //=======================
        // Показ окна
        //=======================

        /*
            Показ готового окна.
         */
        cls.show = function() {
            // если уже открыто - выходим
            if (this.is_opened()) {
                return this;
            }

            if (this.trigger('before_show') === false) {
                return this;
            }

            var current = getCurrentPopup();
            if (current) {
                // подмена старого (открытого) окна новым
                current._beforeHide();
                current._hideInstant();

                try {
                    this._createDOM();
                } catch (err) {
                    this._showScrollbar();
                    this._removeDOM();

                    if (err instanceof ClassError) {
                        this.error(err.message);
                    } else {
                        throw err;
                    }

                    return this;
                }

                this._beforeShow();
                this._showInstant();
            } else {
                // показ нового окна
                this._hideScrollbar();

                try {
                    this._createDOM();
                } catch (err) {
                    this._showScrollbar();
                    this._removeDOM();

                    if (err instanceof ClassError) {
                        this.error(err.message);
                    } else {
                        throw err;
                    }

                    return this;
                }

                this._beforeShow();
                this._showAnimation();
            }

            return this;
        };

        cls._beforeShow = function() {
            currentPopup = this;
            this._opened = true;

            if (this.opts.body_classes) {
                $body.addClass(this.opts.body_classes);
            }
        };

        /*
            Анимация показа
         */
        cls._showAnimation = function() {
            var that = this;
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easingShow,
                complete: function() {
                    that._afterShow();
                }
            });
        };

        /*
            Мгновенный показ окна.
            Используется в случае замены уже существующего видимого окна.
         */
        cls._showInstant = function() {
            this.$container.stop(false, false).show();
            this._afterShow();
        };

        cls._afterShow = function() {
            this._visible = true;

            // кнопки закрытия окна
            var that = this;
            $(document).off('.popup.close').on('click.popup.close', '.' + this.CLOSE_BUTTON_CLASS, function() {
                that.hide();
            });

            this.trigger('after_show');
        };

        //=======================
        // Скрытие окна
        //=======================

        /*
            Скрытие открытого окна.
         */
        cls.hide = function() {
            // если уже закрыто - выходим
            if (!this.is_opened()) {
                return this;
            }

            if (this.trigger('before_hide') === false) {
                return this;
            }

            this._beforeHide();
            this._hideAnimation();
            return this;
        };

        cls._beforeHide = function() {
            this._visible = false;

            // кнопки закрытия окна
            $(document).off('.popup');
        };

        /*
            Анимация скрытия
         */
        cls._hideAnimation = function() {
            var that = this;
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide,
                complete: function() {
                    that._showScrollbar();
                    that._afterHide();
                }
            });
        };

        /*
            Мгновенное скрытие окна.
            Используется в случае замены уже существующего видимого окна.
         */
        cls._hideInstant = function() {
            this.$container.stop(false, false).hide();
            this._afterHide();
        };

        cls._afterHide = function() {
            this._opened = false;
            currentPopup = null;

            if (this.opts.body_classes) {
                $body.removeClass(this.opts.body_classes);
            }

            this.trigger('after_hide');
            this._removeDOM();
        };
    });


    /*
        Модальное окно с оверлеем, кнопкой закрытия
     */
    window.OverlayedPopup = Class(Popup, function OverlayedPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            closeButton: true,
            hideOnClick: true
        });

        cls.OVERLAY_ID = 'popup-overlay';


        /*
            Дополнительные элементы DOM
         */
        cls.extraDOM = function() {
            superclass.extraDOM.call(this);

            this.$overlay = $('<div>').attr('id', this.OVERLAY_ID).hide();
            this.$overlay.addClass(this.opts.classes);
            this.$container.before(this.$overlay);

            if (this.opts.closeButton) {
                this.$closeBtn = $('<div>').addClass(this.CLOSE_BUTTON_CLASS).addClass('popup-close-button');
                this.addCloseButton(this.$closeBtn);
            }

            // Esc press
            if (this.opts.closeButton || this.opts.hideOnClick) {
                var that = this;
                $(document).on('keyup.popup', function(event) {
                    if (event.which === 27 && that.opts.hideOnClick) {
                        that.hide();
                    }
                });
            }
        };

        /*
            Удаление DOM
         */
        cls._removeDOM = function() {
            $('#' + this.OVERLAY_ID).remove();
            superclass._removeDOM.call(this);
        };

        /*
            Добавление кнопки закрытия в DOM
         */
        cls.addCloseButton = function($button) {
            this.$window.prepend($button);
        };

        /*
            Определение того, что клик произошел вне окна и нужно его закрыть (если hideOnClick = true)
         */
        cls.isOutClick = function($target) {
            return $target.closest('body').length && !$target.closest(this.$window).length;
        };

        /*
            Закрытие окна при клике вне модального окна
         */
        cls._afterShow = function() {
            superclass._afterShow.call(this);

            var that = this;
            if (this.opts.hideOnClick) {
                $(document).on('click.popup', function(evt) {
                    if (that.isOutClick($(evt.target)) && that.opts.hideOnClick) {
                        that.hide();
                    }
                });
            }
        };

        /*
            Анимация показа
         */
        cls._showAnimation = function() {
            var that = this;
            this.$overlay.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easingShow
            });
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easingShow,
                complete: function() {
                    that._afterShow();
                }
            });
        };

        /*
            Показ окна в случае замены уже существующего
         */
        cls._showInstant = function() {
            this.$overlay.stop(false, false).show();
            superclass._showInstant.call(this);
        };

        /*
            Анимация скрытия
         */
        cls._hideAnimation = function() {
            var that = this;
            this.$overlay.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide
            });
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide,
                complete: function() {
                    that._showScrollbar();
                    that._afterHide();
                }
            });
        };

        /*
            Скрытие окна в случае замены уже существующего
         */
        cls._hideInstant = function() {
            this.$overlay.stop(false, false).hide();
            superclass._hideInstant.call(this);
        };
    });


    /*
        Алиас создания окна с оверлеем, либо получение текущего окна
     */
    $.popup = function(options) {
        if (options === undefined) {
            return getCurrentPopup();
        } else {
            return OverlayedPopup(options);
        }
    };

})(jQuery);
