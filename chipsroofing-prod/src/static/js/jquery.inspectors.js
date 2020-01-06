(function($) {
    'use strict';

    /*
        Базовый класс инспектирования DOM-элементов.
     */
    var Inspector = function() {};

    Inspector.prototype.defaults = {
        checkOnInit: true,
        beforeCheck: $.noop,
        afterCheck: $.noop
    };

    Inspector.prototype.INSPECT_CLASS = '';
    Inspector.prototype.STATE_DATA_KEY = 'inspector_state';
    Inspector.prototype.OPTS_DATA_KEY = 'inspector_opts';

    /*
        Получение настроек DOM-элемента
     */
    Inspector.prototype.getOpts = function($element) {
        return $element.first().data(this.OPTS_DATA_KEY) || this.defaults;
    };

    /*
        Сохранение настроек DOM-элемента
     */
    Inspector.prototype._setOpts = function($element, opts) {
        $element.first().data(this.OPTS_DATA_KEY, opts).addClass(this.INSPECT_CLASS);
    };

    /*
        Получение состояния DOM-элемента
     */
    Inspector.prototype.getState = function($element) {
        return $element.first().data(this.STATE_DATA_KEY);
    };

    /*
        Сохранение состояния DOM-элемента
     */
    Inspector.prototype._setState = function($element, state) {
        $element.first().data(this.STATE_DATA_KEY, state);
    };

    // ================================================================

    Inspector.prototype._beforeCheck = function($element, opts) {
        opts.beforeCheck.call(this, $element, opts);
    };

    Inspector.prototype._check = function($element, opts) {
        throw Error('not implemented');
    };

    Inspector.prototype._afterCheck = function($element, opts, state) {
        opts.afterCheck.call(this, $element, opts, state);
        this._setState($element, state);
    };

    // ================================================================

    /*
        Функция, проверяющая условие инспектирования на элементах или селекторе
     */
    Inspector.prototype.check = function(elements, options) {
        var that = this;

        var $elements = $(elements);
        $elements.each(function(i, elem) {
            var $elem = $(elem);
            var opts = $.extend({}, that.getOpts($elem), options);

            that._beforeCheck($elem, opts);
            var state = that._check($elem, opts);
            that._afterCheck($elem, opts, state);
        });
    };

    /*
        Добавление селекора элементов для инспектирования
     */
    Inspector.prototype.inspect = function(selector, options) {
        var that = this;
        var $elements = $(selector);
        var opts = $.extend({}, this.defaults, options);

        // если селектор уже инспектируется - удаляем его
        this.ignore(selector);

        // инициализация состояния элементов
        $elements.each(function(i, elem) {
            var $elem = $(elem);
            that._setOpts($elem, opts);
            that._setState($elem, null);

            // сразу проверяем элементы
            if (opts.checkOnInit) {
                that.check($elem);
            }
        });

        return $elements;
    };

    /*
        Удаление селектора из инспектирования
     */
    Inspector.prototype.ignore = function(selector) {
        var that = this;
        $(selector).removeClass(this.INSPECT_CLASS).each(function(i, elem) {
            var $elem = $(elem);
            $elem.removeData(that.OPTS_DATA_KEY + ' ' + that.STATE_DATA_KEY);
        });
    };

    /*
        Проверка всех инспектируемых элементов
     */
    Inspector.prototype.checkAll = function() {
        this.check('.' + this.INSPECT_CLASS);
    };



    /*
        Инспектор, отслеживающий событие, когда ширина окна превысила
        некоторый лимит, либо опустилась ниже него.

        Не следует создавать экземпляры класса MediaInspector.
        Следует пользоваться уже созданным экземпляром $.mediaInspector.

        Параметры:
            point: int  - breakpoint

        Пример:
            $.mediaInspector.inspect('body', {
                point: 768,
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Ширина экрана >= 768');
                    } else {
                        console.log('Ширина экрана < 768');
                    }
                }
            });

            // немедленная проверка элемента
            $.mediaInspector.check('body');

            // удаление элементов из инспектирования
            $.mediaInspector.ignore('body');
     */

    var MediaInspector = function() {};
    MediaInspector.prototype = Object.create(Inspector.prototype);
    MediaInspector.prototype.constructor = MediaInspector;

    MediaInspector.prototype.defaults = $.extend({}, Inspector.prototype.defaults, {
        point: 0
    });

    MediaInspector.prototype.INSPECT_CLASS = 'media-inspect';
    MediaInspector.prototype.STATE_DATA_KEY = 'media_inspector_state';
    MediaInspector.prototype.OPTS_DATA_KEY = 'media_inspector_opts';

    MediaInspector.prototype._check = function($element, opts) {
        return $.winWidth() >= opts.point;
    };

    // Единственный экземпляр инспектора
    $.mediaInspector = new MediaInspector();



    /*
        Инспектор, отслеживающий изменение аспекта картинки по отношению к
        аспекту родительского элемента.

        Не следует создавать экземпляры класса BackgroundInspector.
        Следует пользоваться уже созданным экземпляром $.bgInspector.

        Пример:
            $.bgInspector.inspect('.parallax', {
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Картинка пропорционально шире, чем родительский элемент');
                    } else {
                        console.log('Картинка пропорционально выше, чем родительский элемент');
                    }
                }
            });

            // немедленная проверка элемента
            $.bgInspector.check('.parallax');

            // удаление элементов из инспектирования
            $.bgInspector.ignore('.parallax');
     */

    var BackgroundInspector = function() {};
    BackgroundInspector.prototype = Object.create(Inspector.prototype);
    BackgroundInspector.prototype.constructor = BackgroundInspector;

    BackgroundInspector.prototype.defaults = $.extend({}, Inspector.prototype.defaults, {
        getContainer: function($element) {
            return $element.parent();
        },
        afterCheck: function($elem, opts, state) {
            if (state) {
                $elem.css({
                    width: 'auto',
                    height: '100.6%'
                });
            } else {
                $elem.css({
                    width: '100.6%',
                    height: 'auto'
                });
            }
        }
    });

    BackgroundInspector.prototype.INSPECT_CLASS = 'bg-inspect';
    BackgroundInspector.prototype.STATE_DATA_KEY = 'bg_inspector_state';
    BackgroundInspector.prototype.OPTS_DATA_KEY = 'bg_inspector_opts';

    /*
        Сохраняем inline-стили и сбрасываем размеры
     */
    BackgroundInspector.prototype._beforeCheck = function($element, opts) {
        Inspector.prototype._beforeCheck.call(this, $element, opts);
        $element.data('bginspector_inlines', $element.get(0).style.cssText);
        $element.css({
            width: '',
            height: ''
        });
    };

    BackgroundInspector.prototype._check = function($element, opts) {
        // если проверяется картинка и она еще не загружена,
        // повторяем проверку после загрузки.
        if (($element.prop('tagName') === 'IMG') && !$element.prop('naturalWidth')) {
            var that = this;
            $element.onLoaded(function() {
                if ($element.prop('naturalWidth')) {
                    that.check(this);
                }
            });
        }

        var $parent = opts.getContainer.call(this, $element);
        var elem_asp = $element.outerWidth() / $element.outerHeight();
        var parent_asp = $parent.outerWidth() / $parent.outerHeight();
        $element.data('bginspector_aspect', elem_asp);
        $parent.data('bginspector_aspect', parent_asp);
        return elem_asp >= parent_asp;
    };

    /*
        Восстановление inline-стилей
     */
    BackgroundInspector.prototype._afterCheck = function($element, opts, state) {
        $element.get(0).style.cssText = $element.data('bginspector_inlines') || '';
        Inspector.prototype._afterCheck.call(this, $element, opts, state);
    };

    // Единственный экземпляр инспектора
    $.bgInspector = new BackgroundInspector();



    /*
        Инспектор, отслеживающий событие, когда элемент находится в поле видимости окна.

        Не следует создавать экземпляры класса VisibilityInspector.
        Следует пользоваться уже созданным экземпляром $.visibilityInspector.

        Возбуждает события appear / disappear на инспектируемых элементах.

        Параметры:
            расстояние от соответствующей границы элемента до
            соответствующей границы окна браузера,
            при превышении которого элемент считается видимым/невидимым.

            beforeCheck - функция, вызываемая до проверки
            afterCheck  - функция, вызываемая после проверки

        Пример:
            $.visibilityInspector.inspect('.block', {
                top: 20,
                bottom: 20,
                afterCheck: function($elem, opts, state) {
                    if (state) {
                        console.log('Элемент виден минимум на 20px');
                    } else {
                        console.log('Элемент виден менее, чем на 20px');
                    }
                }
            });

            // немедленная проверка элемента
            $.visibilityInspector.check('.block');

            // удаление элементов из инспектирования
            $.visibilityInspector.ignore('.block');
     */

    var VisibilityInspector = function() {};
    VisibilityInspector.prototype = Object.create(Inspector.prototype);
    VisibilityInspector.prototype.constructor = VisibilityInspector;

    VisibilityInspector.prototype.defaults = $.extend({}, Inspector.prototype.defaults, {
        top: 1,
        right: 1,
        bottom: 1,
        left: 1
    });

    VisibilityInspector.prototype.INSPECT_CLASS = 'visbility-inspect';
    VisibilityInspector.prototype.STATE_DATA_KEY = 'visibility_inspector_state';
    VisibilityInspector.prototype.OPTS_DATA_KEY = 'visibility_inspector_opts';

    VisibilityInspector.prototype._check = function($element, opts) {
        var vpWidth = $.winWidth();
        var vpHeight = $.winHeight();
        var rect = $element.get(0).getBoundingClientRect();

        var invisible_by_top = (rect.top > (vpHeight - opts.top));
        var invisible_by_bottom = (rect.bottom < opts.bottom);
        var invisible_by_left = (rect.left > (vpWidth - opts.left));
        var invisible_by_right = (rect.right < opts.right);

        return !invisible_by_top && !invisible_by_bottom && !invisible_by_left && !invisible_by_right;
    };

    VisibilityInspector.prototype._afterCheck = function($element, opts, state) {
        var old_state = this.getState($element);
        if (old_state !== state) {
            if (state) {
                $element.trigger('appear');
            } else {
                $element.trigger('disappear');
            }
        }

        Inspector.prototype._afterCheck.call(this, $element, opts, state);
    };

    // Единственный экземпляр инспектора
    $.visibilityInspector = new VisibilityInspector();



    $(window).on('scroll.visibility_inspector', $.rared(function() {
        $.visibilityInspector.checkAll();
    }, 100)).on('resize.inspector', $.rared(function() {
        $.mediaInspector.checkAll();
        $.visibilityInspector.checkAll();
        $.bgInspector.checkAll();
    }, 60)).on('load.inspector', function() {
        $.mediaInspector.checkAll();
        $.visibilityInspector.checkAll();
        $.bgInspector.checkAll();
    });

})(jQuery);