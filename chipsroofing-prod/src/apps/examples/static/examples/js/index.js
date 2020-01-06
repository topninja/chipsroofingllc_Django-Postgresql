(function ($) {

    $(document).ready(function () {

        $(document).on('click', '#show_more', function () {
            var preloader = $.preloader(),
                page = $(this).data('page'),
                perpage = $(this).data('perpage');

            $.ajax({
                url: window.js_storage.ajax_examples,
                type: 'GET',
                data: {
                    'page': page,
                    'perpage': perpage
                },
                dataType: 'json',
                success: function (response) {
                    if (response.success_message) {
                        $('#show_more').remove();

                        var $response = $(response.success_message),
                            $items_wrapper = $('#items'),
                            $showmore = null,
                            $items;

                        if ($response.last().attr('id') === 'show_more') {
                            $showmore = $response.last();
                            $items = $response.slice(0, -1);
                        } else {
                            $items = $response;
                        }

                        $items_wrapper.append($items);
                        $items = $('.items');

                        if ($showmore) {
                            $showmore.insertAfter($items_wrapper)
                        }
                        $.scrollTo($items.last(), 800);
                    }
                    preloader.destroy();
                },
                error: $.parseError(function () {
                    preloader.destroy();
                    alert(window.DEFAULT_AJAX_ERROR);
                })
            });
            return false;
        });

        $('.example-wr').magnificPopup({
            delegate: 'a',
            type: 'image',
            tLoading: 'Loading image #%curr%...',
            mainClass: 'mfp-img-mobile',
            gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
            },
            image: {
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                titleSrc: function (item) {
                    return item.el.attr('title');
                }
            }
        });


        var processBlock = function ($block) {
            // слайдер
            var slider = Slider($block.find('.slider'), {
                sliderHeight: Slider.prototype.HEIGHT_MAX,
                itemsPerSlide: function () {
                    var winWidth = $.winWidth();
                    if (winWidth >= 640) {
                        return 2
                    } else {
                        return 1
                    }
                }
            }).attachPlugins([
                SliderSideAnimation({
                    margin: 20
                }),
                SliderDragPlugin({
                    margin: 20
                })
            ]);
        };

        $(document).ready(function () {
            $('#news').each(function () {
                processBlock($(this));
            });
        });

    });

})(jQuery);