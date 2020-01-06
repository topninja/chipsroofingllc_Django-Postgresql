(function($) {

    var color_regex = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i;

    var format_color = function(value) {
        value = value.toString().trim();
        
        var hex;
        if (!(hex = color_regex.exec(value))) {
            return ''
        } else {
            hex = hex[1]
        }

        if (hex.length === 3) {
            var result = '';
            for (var i=0; i<3; i++) {
                var symbol = hex[i];
                result += symbol + symbol;
            }
        } else {
            result = hex
        }
        
        return '#' + result.toUpperCase();
    };

    $(document).on('change', '.colorfield-preview', function() {
        // Изменение цвета в input[color]
        $(this).siblings('.colorfield-hex').val(this.value.toUpperCase())
    }).on('keyup', '.colorfield-hex', function() {
        // Изменение цвета в input[text]
        var self = $(this);
        var value = format_color(self.val());
        self.siblings('.colorfield-preview').val(value || '#000000');
    }).on('focusout', '.colorfield-hex', function() {
        // Завершение редактирования цвета в input[text]
        var self = $(this);
        var value = format_color(self.val());
        self.val(value);
        self.siblings('.colorfield-preview').val(value || '#000000');
    });

})(jQuery);
