(function($) {


$('.video-file').on('click', function () {
            var video = $(this).find('video').get(0),
                videoPreview = $(this).find('.video-preview');
            if (video.paused) {
                video.play();
                videoPreview.hide();
            } else {
                video.pause();
                videoPreview.show();
            }
        });


})(jQuery);