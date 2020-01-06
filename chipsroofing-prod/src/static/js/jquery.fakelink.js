(function($) {

    /*
        Плагин, имитирующий у блока поведение ссылки.
        Ссылка должна находиться внутри блока.

        Зависит от:
            jquery-ui.js

        Параметры:
            itemSelector  - селектор блока, который будет имитировать ссылку
            linkSelector  - селектор ссылки внутри блока

        Пример:
            <div class="block">
              <div class="item">
                <a href="..." class="my-link"></a>
              </div>
              <div class="item">
                <a href="..." class="my-link"></a>
              </div>
            </div>


            $('.block').fakeLink({
                itemSelector: '.item',
                linkSelector: '.my-link'
            });
     */

    $.widget("django.fakeLink", {
        options: {
            itemSelector: null,
            linkSelector: 'a',

            enable: $.noop,
            disable: $.noop,
            destroy: $.noop,
            click: $.noop
        },

        _create: function() {
            // запуск
            this._updateEnabledState();

            // клик на блок
            var that = this;
            this._on(this.element, {
                click: function(event) {
                    var $target = $(event.target);
                    if (this.options.itemSelector) {
                        var $item = $target.closest(that.options.itemSelector);
                        var inside_item = Boolean($item.length);
                    } else {
                        $item = that.element;
                        inside_item = true;
                    }

                    if (!inside_item) {
                        // клик вне блока
                        return
                    }


                    if ($target.is(this.options.linkSelector) || $target.closest(this.options.linkSelector).length) {
                        // клик на целевую ссылку в блоке
                        that._trigger('click', event, {
                            widget: that
                        });
                    } else if (($target.prop('tagName') === 'A') || $target.closest('a').length) {
                        // клик на нецелевую ссылку в блоке

                    } else {
                        // клик на блок
                        that._trigger('click', event, {
                            widget: that
                        });

                        var $link = $item.find(this.options.linkSelector).first();
                        if (!$link.length) {
                            return
                        }

                        var fake_event = new MouseEvent('click', {
                            button: event.button,
                            faked: true,
                            bubbles: true
                        });

                        $link.get(0).dispatchEvent(fake_event);
                        if (!event.faked) {
                            return false;
                        }
                    }
                },
                mousedown: function(event) {
                    if (event.which === 2) {
                        return false;
                    }
                },
                mouseup: function(event) {
                    if (event.which === 2) {
                        that._trigger('click', event, {
                            widget: that
                        });
                        that.link.get(0).dispatchEvent(new MouseEvent('click', {
                            button: 1
                        }));
                    }
                }
            });
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._updateEnabledState();
        },

        _updateEnabledState: function() {
            if (this.options.itemSelector) {
                var $items = this.element.find(this.options.itemSelector);
            } else {
                $items = this.element;
            }

            if (this.options.disabled) {
                this.trigger('disable');
                this._removeClass($items, 'fakelink-item');
            } else {
                this._addClass($items, 'fakelink-item');
                this.trigger('enable');
            }
        },

        _destroy: function() {
            this.trigger('destroy');
        },

        /*
            Вызов событий
         */
        trigger: function(type, data) {
            this._trigger(type, null, $.extend({
                widget: this
            }, data));
        }
    });

})(jQuery);
