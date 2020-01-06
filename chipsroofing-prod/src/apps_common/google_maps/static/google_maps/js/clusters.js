(function($) {
    'use strict';

    /*
        Класс маркера-кластера, объединяющего несколько маркеров.
     */
    window.GMapCluster = Class(GMapCustomMarker, function GMapCluster(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            radius: 60,
            minCount: 2
        });

        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);
            this.markers = [];
            this.bounds = null;
        };

        /*
            Построение DOM
         */
        cls._buildDOM = function() {
            this.$inner = $('<div>').addClass('gmap-cluster-marker');
            this.$counter = $('<span>').addClass('gmap-cluster-text');
            this.$container = $('<div>').addClass('gmap-cluster').append(
                this.$inner.append(this.$counter)
            ).hide();
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            for (var i=0, l=this.markers.length; i<l; i++) {
                this.markers[i].__cluster = null;
            }
            this.markers = [];
            superclass.destroy.call(this);
        };

        /*
            Рассчет области действия кластера
         */
        cls.updateBounds = function() {
            var position = this.position();
            var bounds = new google.maps.LatLngBounds(position.native, position.native);
            this.bounds = this.extendBounds(bounds, this.opts.radius);
            return this;
        };

        /*
            Добавление маркера в кластер
         */
        cls.addMarker = function(marker) {
            if ((marker instanceof window.GMapMarker) || (marker instanceof window.GMapCustomMarker)) {

            } else {
                this.error('marker should be a GMapMarker instance');
                return this;
            }

            if (this.markers.indexOf(marker) >= 0) {
                return this;
            }

            // двигаем кластер на новую позицию
            var total_markers = this.markers.length;
            var marker_position = marker.position();
            if (!total_markers) {
                this.position(marker_position);
            } else {
                var center = this.position();
                var lat = (center.lat * total_markers + marker_position.lat) / (total_markers + 1);
                var lng = (center.lng * total_markers + marker_position.lng) / (total_markers + 1);
                this.position(GMapPoint(lat, lng));
            }
            this.updateBounds();

            marker.__cluster = this;
            this.markers.push(marker);

            total_markers += 1;
            if (total_markers < this.opts.minCount) {
                // минимум не достигнут - показываем маркер
                marker.native.setMap(this.opts.map.native);
            } else if (total_markers === this.opts.minCount) {
                // минимум достигнут - скрываем все маркеры
                for (var i=0, l=this.markers.length; i<l; i++) {
                    this.markers[i].native.setMap(null);
                }

                // показываем себя
                this.$container.show();
            } else {
                // больше минимума - скрываем новый маркер
                marker.native.setMap(null);
            }

            this.$counter.text(total_markers);
        };

        /*
            Удаление маркера из кластера
         */
        cls.removeMarker = function(marker) {
            if ((marker instanceof window.GMapMarker) || (marker instanceof window.GMapCustomMarker)) {

            } else {
                this.error('marker should be a GMapMarker instance');
                return this;
            }

            var total_markers = this.markers.length;

            var index = this.markers.indexOf(marker);
            if (index < 0) {
                return this;
            } else {
                this.markers.splice(index, 1);
            }

            // двигаем кластер на новую позицию
            var marker_position = marker.position();
            if (total_markers > 1) {
                var center = this.position();
                var lat = (center.lat * total_markers - marker_position.lat) / (total_markers - 1);
                var lng = (center.lng * total_markers - marker_position.lng) / (total_markers - 1);
                this.position(GMapPoint(lat, lng));
                this.updateBounds();
            }

            marker.__cluster = null;

            if (total_markers === this.opts.minCount) {
                // оказались ниже минимума - показываем все маркеры
                for (var i = 0, l = this.markers.length; i < l; i++) {
                    this.markers[i].native.setMap(this.opts.map.native);
                }

                // скрываем себя
                this.$container.hide();
            }

            this.$counter.text(total_markers - 1);
        };
    });


    /*
        Класс, обслуживающий маркеры-кластеры.

        Пример:
            var manager = GMapClusterManager({
                map: this,
                markers: this.markers
            }).on('clusterclick', function(cluster) {

            });

     */
    window.GMapClusterManager = Class(GMapOverlayBase, function GMapClusterManager(cls, superclass) {
        cls.defaults = {
            markers: [],
            radius: 60,
            minCount: 2
        };

        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);

            this.ready = false;

            // копия маркеров
            this.markers = this.opts.markers.concat();

            // удаление маркера
            var that = this;
            var destroyMarkerHandler = function() {
                var index = that.markers.indexOf(this);
                if (index >= 0) {
                    that.markers.splice(index, 1);
                }

                if (this.__cluster) {
                    this.__cluster.removeMarker(this);
                }
            };

            for (var i=0, l=this.markers.length; i<l; i++) {
                var marker = this.markers[i];
                marker.__cluster = null;
                marker.on('destroy', destroyMarkerHandler);
            }

            // массив кластеров
            this.clusters = [];
        };

        /*
            Построение DOM
         */
        cls._buildDOM = function() {

        };

        /*
            Событие готовности карты
         */
        cls.onMapReady = function() {
            superclass.onMapReady.call(this);

            // скрываем маркеры
            for (var i=0, l=this.markers.length; i<l; i++) {
                this.markers[i].native.setMap(null);
            }

            this.createClusters();

            var that = this;
            this.opts.map.on('zoom_changed.clusters', function() {
                var map = this;
                var zoom = map.zoom();
                var minZoom = map.minZoom || 0;
                var maxZoom = Math.min(
                    map.maxZoom || 100,
                    map.native.mapTypes[map.native.getMapTypeId()].maxZoom
                );
                zoom = Math.min(Math.max(zoom, minZoom), maxZoom);

                if (that._prevZoom !== zoom) {
                    that._prevZoom = zoom;
                    that.removeClusters();
                }
            }).on('idle.clusters', function() {
                that.createClusters();
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.opts.map.off('.clusters');
            this.removeClusters(true);
            this.markers = [];
        };

        /*
            Удаление всех кластеров
         */
        cls.removeClusters = function(show_markers) {
            for (var i=0, l=this.clusters.length; i<l; i++) {
                this.clusters[i].destroy();
            }
            this.clusters = [];

            if (show_markers) {
                // показываем все маркеры
                for (i=0, l=this.markers.length; i<l; i++) {
                    this.markers[i].native.setMap(this.opts.map.native);
                }
            }
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.onAdd = function() {
            this.ready = true;
        };

        /*
            Рассчет расстояния между точками
         */
        cls._distance = function(p1, p2) {
            if (!p1 || !p2) {
                return 0;
            }

            var R = 6371; // Radius of the Earth in km
            var dLat = (p2.lat - p1.lat) * Math.PI / 180;
            var dLon = (p2.lng - p1.lng) * Math.PI / 180;
            var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(p1.lat * Math.PI / 180) * Math.cos(p2.lat * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c;
        };

        /*
            Создание кластера
         */
        cls._createCluster = function(marker) {
            var cluster = GMapCluster({
                map: this.opts.map,
                position: marker.position(),
                radius: this.opts.radius,
                minCount: this.opts.minCount
            });
            cluster.addMarker(marker);
            this.clusters.push(cluster);

            var that = this;
            cluster.on('click', function() {
                that.trigger('clusterclick', this);
            });

            return cluster;
        };

        /*
            Обработка маркера
         */
        cls.processMarker = function(marker) {
            if (!this.ready || marker.__cluster) {
                return;
            }

            var distance = 40000; // Some large number
            var clusterToAddTo = null;

            var marker_position = marker.position();
            for (var i = 0, l = this.clusters.length; i < l; i++) {
                var cluster = this.clusters[i];
                var d = this._distance(marker_position, cluster.position());
                if (d < distance) {
                    distance = d;
                    clusterToAddTo = cluster;
                }
            }

            if (clusterToAddTo && clusterToAddTo.bounds.contains(marker_position.native)) {
                clusterToAddTo.addMarker(marker);
            } else {
                this._createCluster(marker);
            }
        };

        /*
            Создание и отрисовка кластеров
         */
        cls.createClusters = function() {
            if (!this.ready) {
                return
            }

            var mapBounds = this.opts.map.bounds();
            for (var i=0, l=this.markers.length; i<l; i++) {
                var marker = this.markers[i];
                if (!marker.__cluster && mapBounds.contains(marker.position().native)) {
                    this.processMarker(marker);
                }
            }
        };
    });

})(jQuery);
