(function ($) {

    // Получение координат по адресу в другом поле
    $(document).on('change', '#id_city, #id_address', function () {
        var city = $('#id_city').val();
        var address = $('#id_address').val();
        var gmap = $('#id_coords').next('.google-map').data(GMap.prototype.DATA_KEY);

        gmap.geocode(city + ' ' + address, function (point) {
            var marker = this.markers[0];
            if (marker) {
                marker.position(point);
            } else {
                marker = GMapMarker({
                    map: this,
                    position: point
                })
            }

            marker.trigger('dragend');
            this.panTo(point);
        });
    });

})(jQuery);