(function($) {

    function ChangeImageHeader() {
        if ($('div #wrImage').hasClass('wr-image')){
            var image = $('#fullImage'),
                wrGrid = $('#widthBlock'),
                mgImageBlock = wrGrid .offset().left,
                wBlock = wrGrid.outerWidth(),
                wImage = wBlock + mgImageBlock - 10;

            image.css('width', wImage);
            var hWrImage = image.height();

            if(hWrImage < 420){
                $('#wrImage').css('height', hWrImage);
            }
            else {
                $('#wrImage').css('height', "420px");
            }
        }
    }

    $(window).load(function() {
        ChangeImageHeader();
    });

    $(window).resize(function() {
        ChangeImageHeader();
    });


})(jQuery);