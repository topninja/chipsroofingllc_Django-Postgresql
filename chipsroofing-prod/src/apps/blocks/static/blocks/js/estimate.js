(function($) {

    function ChangeEstimateBlock() {
        var wrGrid = $('.widthBlock'),
            mgBlock = wrGrid.offset().left,
            wBlock = wrGrid.outerWidth();

        if ($("div").is("#icons")) {

            var backgrBlock = $('.background-block'),
                hBlockIcons = $('#icons'),
                wIcons = wBlock + mgBlock - 10,
                hWrIcons = hBlockIcons.outerHeight();

            backgrBlock.css({
                'height': hWrIcons,
                'width': wIcons
            });
        }

        if ($("div").is("#estimate")) {

            var shadowBlock = $('.shadow-block'),
             hBlockEstimate = $('#estimate'),
            wEstimate = wBlock + mgBlock - 10,
            hWrEstimate = hBlockEstimate.outerHeight();

           shadowBlock.css({
                'height': hWrEstimate,
                'width': wEstimate
            });
        }
    }

    $(document).ready(function() {
        ChangeEstimateBlock();
    });

    $(window).resize(function() {
        ChangeEstimateBlock();
    });

})(jQuery);

