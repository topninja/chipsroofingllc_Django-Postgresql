(function() {

    /*
        Модальное окно с прелоадером.
        Возвращает Deferred-объект анимации показа.

        Требует:
            jquery.utils.js, jquery.popups.js
     */
    var addPreloader = function($container) {
        var $preloader = $('<div>').addClass('preloader');
        $container.append($preloader);
    };

    $.preloader = function(options) {
        var opts = $.extend(true, {
            classes: 'popup-preloader',
            content: function() {
                addPreloader(this.$content);
            },
            closeButton: false,
            hideOnClick: false
        }, options);

        var popup = OverlayedPopup(opts);
        return popup && popup.show();
    };

    /*
        Показ/скрытие прелоадера над текущим окном.

        Требует:
            jquery.utils.js, jquery.popups.js
     */
    $.popup.showPreloader = function() {
        var popup = $.popup();
        if (!popup) {
            return
        }

        var $preloaderHolder = popup.$window.find('.preloader-overlay');
        if (!$preloaderHolder.length) {
            $preloaderHolder = $('<div>').addClass('preloader-overlay').appendTo(popup.$window);
            addPreloader($preloaderHolder);
        }

        if (typeof popup._origHideOnClick === "undefined") {
            popup._origHideOnClick = popup.opts.hideOnClick;
            popup.opts.hideOnClick = false;
        }

        popup.$container.find('.' + popup.CLOSE_BUTTON_CLASS).hide();
        popup.$container.addClass('popup-preloader-overlay');
    };

    $.popup.hidePreloader = function() {
        var popup = $.popup();
        if (!popup) {
            return
        }

        if (typeof popup._origHideOnClick !== "undefined") {
            popup.opts.hideOnClick = popup._origHideOnClick;
            delete popup._origHideOnClick;
        }

        popup.$container.find('.' + popup.CLOSE_BUTTON_CLASS).show();
        popup.$container.removeClass('popup-preloader-overlay');
    }

})(jQuery);
