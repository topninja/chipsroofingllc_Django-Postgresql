(function($) {
    'use strict';

    /*
        Базовый класс всплывающего окна.

        Задает положение на карте, DOM-разметку и содержимое.

        Генерируемые события:
            added   - DOM добавлен на карту
            open    - после открытия окна
            close   - после закрытия окна

     */

    // события, не всплывающие на окне
    var MOUSE_EVENTS = [
        'mousedown', 'mousemove', 'mouseover', 'mouseout', 'mouseup',
        'mousewheel', 'DOMMouseScroll', 'touchstart', 'touchend', 'touchmove',
        'dblclick', 'contextmenu', 'click'
    ];

    window.GMapBalloonBase = Class(GMapOverlayBase, function GMapBalloonBase(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            content: '',
            position: null
        });

        cls.layer = 'floatPane';

        cls.NATIVE_EVENTS = [
            'domready',
            'closeclick',
            'content_changed',
            'position_changed'
        ];


        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);

            // точка
            this._position = this.opts.position;
            if (this._position) {
                if (this._position instanceof GMapPoint === false) {
                    return this.raise('position should be a GMapPoint instance');
                }
            }

            // состояние
            this._opened = false;

            // контент
            this._content = null;
        };

        /*
            Построение DOM
         */
        cls._buildDOM = function() {
            this.$container = $('<div>').addClass('gmap-balloon').hide();
            this.$content = $('<div>').addClass('gmap-balloon-content');
            this.$closeBtn = $('<div>').addClass('gmap-balloon-close');

            this.$container.append(this.$closeBtn, this.$content);
        };

        /*
            Событие готовности карты
         */
        cls.onMapReady = function() {
            superclass.onMapReady.call(this);
            this.content(this.opts.content);
        };

        /*
            Рассчет размеров окна
         */
        cls.updateSize = function() {
            this.$container.css({
                width: '',
                height: ''
            });

            this._width = this.$container.outerWidth();
            this._height = this.$container.outerHeight();

            this.$container.css({
                width: this._width
            });
        };

        /*
            Позиционирование окна
         */
        cls.updatePosition = function() {
            if (!this._opened) {
                return
            }

            if (!this._position) {
                this.error('position required');
                return
            }

            var projection = this.native.getProjection();
            var pos = projection.fromLatLngToDivPixel(this.position().native);
            this._updatePosition(pos);
        };

        /*
            Позиционирование окна
         */
        cls._updatePosition = function(pos) {
            this.$container.css({
                left: pos.x - this._width / 2,
                top: pos.y - this._height
            });
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.onAdd = function() {
            superclass.onAdd.call(this);

            // закрытие окна при клике на крестик
            var that = this;
            this._closeListener = google.maps.event.addDomListener(this.$closeBtn.get(0), 'click', function() {
                that.close();
                google.maps.event.trigger(that.native, 'closeclick');
            });

            // Запрещаем всплытие некоторых событий на окне, чтобы можно было выделять текст
            this._listeners = [];
            MOUSE_EVENTS.forEach(function(eventname) {
                var handler = google.maps.event.addDomListener(
                    that.$container.get(0),
                    eventname,
                    function(e) {
                        e.cancelBubble = true;
                        if (e.stopPropagation) {
                            e.stopPropagation();
                        }
                    }
                );
                that._listeners.push(handler);
            });

            google.maps.event.trigger(this.native, 'domready');
            this.trigger('added');
        };

        /*
            Отрисовка оверлея
         */
        cls.draw = function() {
            this.updatePosition();
        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.onRemove = function() {
            // удаление обработчиков мыши на окне
            this._listeners.forEach(function(handler) {
                google.maps.event.removeListener(handler);
            });

            google.maps.event.removeListener(this._closeListener);
            superclass.onRemove.call(this);
        };

        /*
            Событие загрузки картинки
         */
        cls.onImageLoaded = function() {
            this.updateSize();
            this.updatePosition()
        };

        /*
            Показ окна
         */
        cls.open = function() {
            if (this._opened) {
                return false
            } else {
                this._opened = true;
            }

            var that = this;
            var args = Array.prototype.slice.call(arguments);
            setTimeout(function() {
                that.updatePosition();
                that._open.apply(that, args);
            }, 0);
        };

        /*
            Анимация показа окна
         */
        cls._open = function() {
            var that = this;
            this.$container.hide().fadeIn({
                duration: 100,
                complete: function() {
                    that.trigger('open');
                }
            });
        };

        /*
            Закрытие окна
         */
        cls.close = function() {
            if (!this._opened) {
                return false
            } else {
                this._opened = false;
            }

            this._close.apply(this, arguments);
        };

        /*
            Анимация закрытия окна
         */
        cls._close = function() {
            var that = this;
            this.$container.fadeOut({
                duration: 100,
                complete: function() {
                    that.trigger('close');
                }
            });
        };

        /*
            Получение / установка положения
         */
        cls.position = function(value) {
            if (value === undefined) {
                // получение положения
                return this._position;
            }

            if (value) {
                if (value instanceof GMapPoint === false) {
                    this.error('value should be a GMapPoint instance');
                    return this;
                }

                this._position = value;
                this.updatePosition();
                google.maps.event.trigger(this.native, 'position_changed');
            }

            return this;
        };

        /*
            Получение / установка содержимого всплывающего окна
         */
        cls.content = function(value) {
            if (value === undefined) {
                // получение содержимого
                return this._content;
            }

            if (value && (typeof value !== 'string')) {
                this.error('value should be a string');
                return this;
            }

            if (this._content === null) {
                // установка контента при инициализации
                this._content = value;
                this.$content.html(this._content);
            } else {
                // установка контента после инициализации
                this._content = value;
                this.$content.html(this._content);

                this.updateSize();
                this.updatePosition();
                google.maps.event.trigger(this.native, 'content_changed');
            }

            // перерисовка при загрузке картинок
            var that = this;
            this.$container.find('img').on('load', function() {
                that.onImageLoaded();
            });

            return this;
        };
    });


    /*
        Всплывающее окно, привязанное к маркеру
     */
    window.GMapBalloon = Class(window.GMapBalloonBase, function GMapBalloon(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            autoPan: true
        });

        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);

            // привязка к маркеру
            this._anchor = null;
        };

        /*
            Построение DOM
         */
        cls._buildDOM = function() {
            superclass._buildDOM.call(this);

            this.$arrow = $('<div>').addClass('gmap-balloon-arrow');
            this.$container.append(this.$arrow);
        };

        /*
            Событие загрузки картинки
         */
        cls.onImageLoaded = function() {
            if (this.opts.autoPan) {
                this.panToView()
            }

            this.updateSize();
            this.updatePosition();
        };

        /*
            Показ окна
         */
        cls.open = function(marker) {
            if (!marker) {
                this.error('marker required');
                return
            } else if (marker instanceof GMapMarker === false) {
                this.error('marker should be a GMapMarker instance');
                return
            }

            // отвязывание события со старого маркера
            if (this._anchor) {
                this._anchor.off('.balloon');
            }

            this._anchor = marker;
            this.position(this._anchor.position());

            var that = this;
            this._anchor.one('detached.balloon', function() {
                // закрываем окно при удалении маркера с карты
                that._anchor = null;
                that.close();
            });
            this._anchor.on('dragend.balloon', function() {
                // меняем положение окна при перемещении маркера
                var anchor = this;
                that.position(anchor.position());
            });

            superclass.open.call(this);
        };

        /*
            Анимация показа окна
         */
        cls._open = function() {
            if (this.opts.autoPan) {
                this.panToView()
            }

            superclass._open.call(this);
        };

        /*
            Позиционирование окна
         */
        cls._updatePosition = function(pos) {
            this.$container.css({
                left: pos.x - this._width / 2,
                top: pos.y - this._height - this._getAnchorHeight()
            });
        };

        /*
            Перемещение карты к окну
         */
        cls.panToView = function() {
            if (!this._opened) {
                return
            }

            this.updateSize();

            var map = this.map();
            var mapDiv = map.native.getDiv();
            var mapHeight = mapDiv.offsetHeight;

            var latLng = this.position().native;
            var projection = this.native.getProjection();

            var centerPos = projection.fromLatLngToContainerPixel(map.center().native);
            var coords = projection.fromLatLngToContainerPixel(latLng);

            var anchorHeight = this._getAnchorHeight();
            var totalHeight = this._height + anchorHeight;
            if (totalHeight < mapHeight) {
                coords.y -= Math.min(totalHeight / 2, centerPos.y - anchorHeight);
            }

            latLng = projection.fromContainerPixelToLatLng(coords);

            map.panTo(GMapPoint.fromNative(latLng));
        };

        /*
            Получение высоты маркера
         */
        cls._getAnchorHeight = function() {
            if (!this._anchor) {
                return
            }

            var icon = this._anchor.icon();
            if (icon) {
                if (icon.scaledSize) {
                    var offset_y =  icon.scaledSize.height;
                } else if (icon.size) {
                    offset_y = icon.size.height;
                }

                if (icon.anchor) {
                    offset_y -= parseInt(icon.anchor.y) || 0;
                }

                return offset_y;
            }

            return 40;
        }
    });

})(jQuery);
