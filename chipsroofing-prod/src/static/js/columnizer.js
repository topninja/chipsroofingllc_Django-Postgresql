(function($) {

    /*
        Оптимальная разбивка элементов по колонкам.

        Зависит от:
            jquery-ui.js

        Пример:
            HTML:
                <div id="block">
                    <div class="item">...</div>
                    <div class="item">...</div>
                    ...
                    <div class="item">...</div>
                </div>

            JS:
                $('#block').columnizer({
                    columns: 2,
                    selector: '.item'
                });

                // изменение кол-ва колонок
                $('#block').columnizer('setColumns', 3);
     */

    var arraySum = function (array) {
        return array.reduce(function(a, b) { return a+b });
    };

    var reduceColumn = function(columns, index) {
        if (index <= 1) return false;
        columns[index-1] = columns[index-1].concat(columns[index].splice(0, 1));
        return true;
    };

    $.widget("django.columnizer", {
        options: {
            columns: 2,
            selector: '',

            enable: function(event, data) {
                var that = data.widget;
                that.setColumns(that.options.columns);
                that._addClass(that.element, 'columnizer');
            },
            disable: function(event, data) {
                var that = data.widget;
                that.setColumns(0);
                that._removeClass(that.element, 'columnizer');
            },
            destroy: function(event, data) {
                var that = data.widget;
                that.setColumns(0);
                that._removeClass(that.element, 'columnizer');
            }
        },

        _create: function() {
            // запуск
            this._updateEnabledState();
        },

        _setOption: function(key, value) {
            if (key === "columns" ) {
                this.setColumns(value);
            }
            this._super(key, value);
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._updateEnabledState();
        },

        _updateEnabledState: function() {
            if (this.options.disabled) {
                this.trigger('disable');
            } else {
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
        },


        /*
            Возвращает элементы для их разбивки
         */
        _getItems: function() {
            return this.element.find(this.options.selector);
        },

        /*
            Возвращает массив высот элементов
         */
        _getItemHeights: function($items) {
            return $items.toArray().map(function(elem) {
                return $(elem).outerHeight(true);
            });
        },

        /*
            Построение карты разделения элементов.
            Возвращает массив массивов, содержащих высоты элементов
         */
        _getMap: function(heights, column_count) {
            // средняя высота колонки
            var average = arraySum(heights) / column_count;

            var map = [];
            var column_index = -1;
            while (++column_index < column_count) {
                if (column_index === column_count - 1) {
                    // последняя колонка - добавляем все оставшиеся элементы
                    map.push(heights);
                    break;
                }

                // формируем колонку с минимальным отклонением от среднего
                var height = 0;
                var deviation = average;
                var item_index = 0;
                var total_count = heights.length;
                while (item_index < total_count) {
                    var item_height = heights[item_index];
                    var next_deviation = Math.abs(average - height - item_height);

                    // отклонение уменьшилось или это первый элемент
                    if ((next_deviation <= deviation) || !height) {
                        deviation = next_deviation;
                        height += item_height;
                        item_index++;
                    } else {
                        break
                    }
                }

                map.push(heights.splice(0, item_index));
            }

            // вторая итерация
            var maxSum = 0;
            var maxIndex = -1;
            $.each(map, function(index, column) {
                var sum = arraySum(column);
                if (sum >= maxSum) {
                    maxSum = sum;
                    maxIndex = index;
                }
            });

            var currentIndex = maxIndex;
            var clone_map = [].concat(map);
            while (true) {
                if (currentIndex <= 1) break;
                reduceColumn(clone_map, currentIndex);
                var currentSum = arraySum(clone_map[currentIndex]);
                var previousSum = arraySum(clone_map[currentIndex-1]);
                if ((currentSum <= maxSum) && (previousSum <= maxSum)) {
                    map = clone_map;
                    break;
                }
                currentIndex--;
            }

            return map;
        },

        /*
            Создание контейнера колонки элементов
         */
        _cleateItemsColumn: function($column_items) {
            return $('<div/>').addClass('column').append($column_items);
        },

        /*
            Формирование колонок
         */
        setColumns: function(column_count) {
            var $items = this._getItems();
            var heights = this._getItemHeights($items);
            $items.detach();
            this.element.empty();

            column_count = parseInt(column_count);
            if (column_count <= 0) {
                this.element.append($items);
                return [];
            }

            var map = this._getMap(heights, column_count);
            for (var i=0, l=map.length; i<l; i++) {
                this.element.append(
                    this._cleateItemsColumn($items.splice(0, map[i].length))
                );
            }
            return map;
        }
    });

})(jQuery);
