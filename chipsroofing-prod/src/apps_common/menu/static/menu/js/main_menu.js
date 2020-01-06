(function($) {
    'use strict';

    /*
        Класс, отвечающий за показ/скрытие меню при нажатии кнопки.

        Требует:
            jquery.utils.js

        Параметры:
            menuSelector        - селектор элемента меню
            buttonSelector      - селектор кнопки, активирующей меню
            openedClass         - класс body, когда меню открыто
            fullHeight          - должно ли меню быть на всю высоту

        События:
            // Перед показом мобильного меню
            before_open

            // Перед скрытием мобильного меню
            before_close

            // Изменение размера окна
            resize
    */

    var MainMenu = Class(EventedObject, function MainMenu(cls, superclass) {
        cls.init = function(options) {
            superclass.init.call(this);

            this.opts = $.extend({
                menuSelector: '.mobile-menu',
                buttonSelector: '#mobile-menu-button',
                openedClass: 'main-menu-opened',

                fullHeight: false
            }, options);

            // клик на кнопку
            var that = this;
            $(document).off('.menu').on('click.menu', this.opts.buttonSelector, function() {
                if (that.isOpened()) {
                    return that.close();
                } else {
                    return that.open();
                }
            });
        };

        cls.getMenu = function() {
            return $(this.opts.menuSelector).first();
        };

        cls.isOpened = function() {
            return $('body').hasClass(this.opts.openedClass);
        };

        cls._open = function() {
            return $('body').addClass(this.opts.openedClass);
        };

        cls._close = function() {
            return $('body').removeClass(this.opts.openedClass);
        };

        cls.update = function() {
            var $menu = this.getMenu();
            if (!$menu.length) {
                return false;
            }

            // на всю высоту окна
            if (this.opts.fullHeight) {
                $menu.height('auto');
                var default_height = $menu.outerHeight();
                $menu.outerHeight(Math.max(default_height, $.winHeight()));
            }
        };

        /*
            Показ меню
         */
        cls.open = function() {
            var $menu = this.getMenu();
            if (!$menu.length) {
                return false;
            }

            if (this.trigger('before_open') === false) {
                return false;
            }

            this.update();
            this._open();
        };

        /*
            Скрытие меню
         */
        cls.close = function() {
            var $menu = this.getMenu();
            if (!$menu.length) {
                return false;
            }

            if (this.trigger('before_close') === false) {
                return false;
            }

            this._close();
        };
    });


    $(document).ready(function() {
        window.main_menu = MainMenu({
            fullHeight: false
        }).on('resize', function(winWidth) {
            // скрытие на больших экранах
            if (winWidth >= 768) {
                this.close();
            }
        }).on('before_open', function() {
            $.scrollTo(0, 400);
        });
    });

    $(window).on('resize.menu', $.rared(function() {
        if (!window.main_menu) {
            return
        }

        window.main_menu.update();
        window.main_menu.trigger('resize', $.winWidth());
    }, 100));

})(jQuery);
