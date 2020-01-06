(function($) {
    'use strict';

    /*
        Генерирует события перетаскивания. Реального перемещения не делает.
        Это только интерфейс для реализации разных штук.

        Возможность продолжения движения по инерции при отпускании кнопки мыши.

        Зависит от:
            jquery.utils.js

        Параметры:
            preventDrag: true/false           - предотвратить событие drag по-умолчанию
            preventClick: true/false          - предотвратить событие click при перетаскивании
            mouse: true                       - разрешить перетаскивание мышью
            touch: true                       - разрешить перетаскивание тачпадом
            ignoreDistanceX: 18               - игнорировать краткие движения по оси X
            ignoreDistanceY: 18               - игнорировать краткие движения по оси Y
            momentum: true                    - добавлять движение по инерции
            momentumLightness: 500            - "легкость" инерции (0 - нет инерции)
            momentumEasing: 'easeOutCubic'    - функция сглаживания инерционного движения

        События:
            // Нажатие кнопки мыши (касание пальцем)
            mousedown(evt)

            // Начало перетаскивания. Если вернет false - перетаскивание не начнется
            dragstart(evt)

            // Процесс перетаскивания.
            drag(evt)

            // Завершение перетаскивания.
            dragend(evt)

            // Отпускание кнопки мыши (пальца)
            mouseup(evt)

            // Начало инерционного движения. Если вернет false - инерционное движение отменяется
            start_momentum(momentum)

            // Окончание инерционного движения
            stop_momentum()

        Примеры:
            var drager = Drager(element, {

            }).on('mousedown', function(evt) {

                // блокировка всплытия события mousedown или touchstart
                return false;
            }).on('drag', function(evt) {

                // блокировка всплытия события mousemove или touchmove
                return false;
            }).on('start_momentum', function(momentum) {
                // Модификация параметров инерционного движения
                momentum.setSpeed(undefined, 1);
                momentum.setLightness(600);
                momentum.setEndPoint(200, 400);
                momentum.setDuration(2000);
                momentum.setEasing('linear');

                // отмена инерционного движения
                return false;
            }).on('mouseup', function(evt) {

                // блокировка всплытия события mouseup или touchend
                return false;
            })
    */

    /** @namespace event.originalEvent.changedTouches */
    /** @namespace window.navigator.msPointerEnabled */

    var touchstart = window.navigator.msPointerEnabled ? 'MSPointerDown' : 'touchstart';
    var touchmove = window.navigator.msPointerEnabled ? 'MSPointerMove' : 'touchmove';
    var touchend = window.navigator.msPointerEnabled ? 'MSPointerUp' : 'touchend';

    var getDx = function(fromPoint, toPoint) {
        var clientDx = toPoint.clientX - fromPoint.clientX;
        var pageDx = toPoint.pageX - fromPoint.pageX;
        return (clientDx || pageDx) >= 0 ? Math.max(clientDx, pageDx) : Math.min(clientDx, pageDx);
    };

    var getDy = function(fromPoint, toPoint) {
        var clientDy = toPoint.clientY - fromPoint.clientY;
        var pageDy = toPoint.pageY - fromPoint.pageY;
        return (clientDy || pageDy) >= 0 ? Math.max(clientDy, pageDy) : Math.min(clientDy, pageDy);
    };

    var isMultiTouch = function(event) {
        var orig = event.originalEvent;
        var touchPoints = (typeof orig.changedTouches !== 'undefined') ? orig.changedTouches : [orig];
        return touchPoints.length > 1;
    };

    var getTouchPoint = function(event) {
        var orig = event.originalEvent;
        if (typeof orig.changedTouches !== 'undefined') {
            return orig.changedTouches[0]
        } else {
            return orig
        }
    };

    // ===============================================

    /*
        Движение по инерции
     */
    var Momentum = Class(Object, function Momentum(cls, superclass) {
        cls.init = function(drager, event, momentumPoint) {
            this.lightness = drager.opts.momentumLightness;
            this.easing = drager.opts.momentumEasing;
            this.startX = event.dx;
            this.startY = event.dy;
            this.speedX = 0;
            this.speedY = 0;
            this.duration = 0;

            var dx = getDx(momentumPoint.point, event.point);
            var dy = getDy(momentumPoint.point, event.point);
            var duration = event.origEvent.timeStamp - momentumPoint.timeStamp;
            this.setSpeed(dx / duration, dy / duration);
        };

        cls.setSpeed = function(speedX, speedY) {
            if (typeof speedX !== 'undefined') {
                this.speedX = speedX;
            }
            if (typeof speedY !== 'undefined') {
                this.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        cls.setDuration = function(duration) {
            this.duration = Math.abs(duration) || 0;
            this.endX = this.startX + this.speedX * this.duration;
            this.endY = this.startY + this.speedY * this.duration;
        };

        cls.setLightness = function(lightness) {
            this.lightness = lightness;

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        cls.setEndPoint = function(endX, endY) {
            var dx = endX - this.startX;
            var dy = endY - this.startY;
            var tx = this.speedX ? Math.abs(dx / this.speedX) : 0;
            var ty = this.speedY ? Math.abs(dy / this.speedY) : 0;

            this.duration = Math.max(tx, ty) || 0;
            this.endX = endX;
            this.endY = endY;
        };

        cls.setEasing = function(easing) {
            this.easing = easing;
        };
    });

    // ===============================================

    var DragerEvent = Class(Object, function DragerEvent(cls, superclass) {
        cls.init = function(event, drager) {
            var mouseEvent = event;
            if (event.type.substr(0, 5) === 'touch') {
                mouseEvent = getTouchPoint(event);
            }

            this.origEvent = event;
            this.target = drager.$element.get(0);
            this.timeStamp = event.timeStamp;
            this.point = {
                pageX: mouseEvent.pageX,
                pageY: mouseEvent.pageY,
                clientX: mouseEvent.clientX,
                clientY: mouseEvent.clientY
            }
        };
    });

    var MouseDownDragerEvent = Class(DragerEvent, function MouseDownDragerEvent(cls, superclass) {
        cls.init = function(event, drager) {
            superclass.init.call(this, event, drager);

            this.dx = 0;
            this.dy = 0;
            this.abs_dx = 0;
            this.abs_dy = 0;
        };
    });

    var MouseMoveDragerEvent = Class(DragerEvent, function MouseMoveDragerEvent(cls, superclass) {
        cls.init = function(event, drager) {
            superclass.init.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };
    });

    var MouseUpDragerEvent = Class(DragerEvent, function MouseUpDragerEvent(cls, superclass) {
        cls.init = function(event, drager) {
            superclass.init.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };
    });

    // ===============================================

    var dragerID = 0;
    window.Drager = Class(EventedObject, function Drager(cls, superclass) {
        cls.defaults = {
            preventDrag: true,
            preventClick: true,

            mouse: true,
            touch: true,
            ignoreDistanceX: 18,
            ignoreDistanceY: 18,
            momentum: true,
            momentumLightness: 500,
            momentumEasing: 'easeOutCubic',
            minMomentumDuration: 100
        };


        cls.init = function(element, options) {
            superclass.init.call(this);

            this.$element = $(element).first();
            if (!this.$element.length) {
                return this.raise('root element not found');
            }

            this.opts = $.extend({}, this.defaults, options);


            this.id = dragerID++;

            // Был ли перемещен элемент (для обработки случаев клика и ignoreDistance)
            this.wasDragged = false;

            // Защита от дублирования событий
            this._dragging_allowed = false;

            // Точки, на основани которых будет вычислена скорость инерциального движения
            this._momentumPoints = [];

            // Точка начала перемещения
            this.startPoint = null;

            // === Инициализация ===
            this.attach();
        };

        cls.destroy = function() {
            this.detach();
            superclass.destroy.call(this);
        };

        // ================================================

        /*
            Добавление точки вычисления инерции
         */
        cls._addMomentumPoint = function(evt) {
            if (this._momentumPoints.length) {
                // Если недавно уже добавляли - выходим
                var lastPoint = this._momentumPoints[this._momentumPoints.length - 1];
                if (evt.timeStamp - lastPoint.timeStamp < 200) {
                    return
                }
            }

            var record = {
                point: evt.point,
                timeStamp: evt.timeStamp
            };

            if (this._momentumPoints.length === 2) {
                this._momentumPoints.shift();
            }
            this._momentumPoints.push(record);
        };

        /*
            Получение точки вычисления инерции
         */
        cls._getMomentumPoint = function(evt) {
            if (!this._momentumPoints.length) {
                return
            }

            var lastPoint = this._momentumPoints[this._momentumPoints.length - 1];
            if (evt.timeStamp - lastPoint.timeStamp < 100) {
                if (this._momentumPoints.length === 2) {
                    lastPoint = this._momentumPoints[0];
                }
            }
            return lastPoint;
        };

        /*
            Запуск инерционного движения
          */
        cls.startMomentum = function(evt) {
            if (!(evt.momentum instanceof Momentum)) {
                return false;
            }

            if (this.trigger('start_momentum', evt.momentum) === false) {
                return false;
            }

            var that = this;
            this._momentumAnimation = $({
                x: evt.momentum.startX,
                y: evt.momentum.startY
            }).animate({
                x: evt.momentum.endX,
                y: evt.momentum.endY
            }, {
                duration: evt.momentum.duration,
                easing: evt.momentum.easing,
                progress: function() {
                    evt.dx = this.x;
                    evt.dy = this.y;
                    evt.timeStamp = $.now();
                    that.trigger('drag', evt);
                },
                complete: function() {
                    that._momentumAnimation = null;
                    that.trigger('stop_momentum');
                }
            });
        };

        /*
            Остановка инерционного движения
          */
        cls.stopMomentum = function(jumpToEnd) {
            if (this._momentumAnimation) {
                this._momentumAnimation.stop(true, jumpToEnd);

                if (!jumpToEnd) {
                    this._momentumAnimation = null;
                    this.trigger('stop_momentum');
                }
            }
        };

        /*
            Сброс начала отсчета передвижения
          */
        cls.setStartPoint = function(evt) {
            this.startPoint = evt.point;
        };

        /*
            Прекращение отслеживания текущего сеанса перемещения
          */
        cls.stopCurrent = function(evt) {
            this._dragging_allowed = false;

            if (this.wasDragged) {
                this.wasDragged = false;

                // Вычисление параметров инерции
                if (this.opts.momentum) {
                    var lastPoint = this._getMomentumPoint(evt);
                    if (lastPoint) {
                        evt.momentum = Momentum(this, evt, lastPoint);
                    }
                }

                this.trigger('dragend', evt);
            }

            // запуск инерции
            if ((evt.momentum instanceof Momentum) &&
                (evt.momentum.duration >= this.opts.minMomentumDuration)) {
                this.startMomentum(evt);
            }

            return this.trigger('mouseup', evt);
        };

        // ================
        // === Handlers ===
        // ================

        cls.mouseDownHandler = function(event) {
            if ((event.type === 'mousedown') && (event.button !== 0)) return;

            var evt = MouseDownDragerEvent(event, this);
            this.wasDragged = false;
            this._dragging_allowed = true;
            this._momentumPoints = [];
            this._addMomentumPoint(evt);

            this.$start_target = $(event.target);

            this.setStartPoint(evt);
            return this.trigger('mousedown', evt);
        };

        cls.dragHandler = function(event) {
            if (!this._dragging_allowed) return;

            var evt = MouseMoveDragerEvent(event, this);
            this._addMomentumPoint(evt);

            if (!this.wasDragged) {
                if ((evt.abs_dx > this.opts.ignoreDistanceX) || (evt.abs_dy > this.opts.ignoreDistanceY)) {
                    if (this.trigger('dragstart', evt) === false) {
                        return
                    }
                    this.wasDragged = true;

                    if (this.opts.preventClick) {
                        this.$start_target.one('click.drager.prevent' + this.id, function() {
                            return false
                        });
                    }
                } else {
                    return;
                }
            }

            return this.trigger('drag', evt);
        };

        cls.mouseUpHandler = function(event) {
            if (!this._dragging_allowed) return;

            if (this.wasDragged) {
                // предотвращаем событие click при перемещении.
                if (this.opts.preventClick) {
                    // гарантия отключения перехватчика, если mouseup был вызван через trigger
                    var that = this;
                    setTimeout(function() {
                        that.$start_target.off('click.drager.prevent' + that.id);
                    }, 0);
                }
            }

            var evt = MouseUpDragerEvent(event, this);
            return this.stopCurrent(evt);
        };

        // ================
        // ==== Events ====
        // ================

        // Удаление обработчиков событий
        cls.detach = function() {
            // Отвязываем все события, связанные с объектом
            this.$element.off('.drager' + this.id);
            $(document).off('.drager' + this.id);
        };

        // Привязка обработчиков событий
        cls.attach = function() {
            var that = this;

            this.detach();

            // ====================
            // === Mouse Events ===
            // ====================
            if (this.opts.mouse) {
                // Блокируем дефолтовый Drag'n'Drop браузера
                if (this.opts.preventDrag) {
                    this.$element.on('dragstart.drager.prevent' + this.id, function() {
                        return false;
                    });
                }

                this.$element.on('mousedown.drager' + this.id, function(event) {
                    return that.mouseDownHandler.call(that, event);
                });

                $(document).on('mousemove.drager' + this.id, function(event) {
                    return that.dragHandler.call(that, event);
                }).on('mouseup.drager' + this.id, function(event) {
                    return that.mouseUpHandler.call(that, event);
                });
            }

            // ====================
            // === Touch Events ===
            // ====================
            if (this.opts.touch) {
                var ns = 'drager' + this.id;

                this.$element.on(touchstart + '.' + ns, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseDownHandler.call(that, event);
                });
                $(document).on(touchmove + '.' + ns, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.dragHandler.call(that, event);
                }).on(touchend + '.' + ns, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseUpHandler.call(that, event);
                });
            }
        };
    });

})(jQuery);
