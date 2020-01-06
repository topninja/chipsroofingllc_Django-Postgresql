(function($) {

    function getInternetExplorerVersion()
    {
        var rv = -1;
        if (navigator.appName == 'Microsoft Internet Explorer')
        {
            var ua = navigator.userAgent;
            var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
            if (re.exec(ua) != null)
                rv = parseFloat( RegExp.$1 );
        }
        else if (navigator.appName == 'Netscape')
        {
            var ua = navigator.userAgent;
            var re  = new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})");
            if (re.exec(ua) != null)
                rv = parseFloat( RegExp.$1 );
        }
        return rv;
    }

    if(getInternetExplorerVersion()!==-1){
        $('svg').addClass('svg-ie');
        if($(window).width() > 768){
            $('.homeDescImg').css('display', 'block');
            $('.homeMobImg').css('display', 'none');
        }
        else  {
            $('.homeMobImg').css('display', 'block');
            $('.homeDescImg').css('display', 'none');
        }
    }

    var wow = new WOW(
        {
            boxClass:     'wow',      // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            mobile:       true,       // trigger animations on mobile devices (default is true)
            delay: 2000,
        }
    );
    function changeWowDelay(selector, value1, value2) {
        var selectorwow = $("." + selector);

        $(window).scrollTop() > (selectorwow.offset().top - $(window).height()) ?
            $(selectorwow).attr("data-wow-delay", value1 + 's') : $(selectorwow).attr("data-wow-delay", value2 + 's');

    }

    function changeHeightHome(){
        var heigthTitleService = $(".title-part").innerHeight();

        $(".section-header").css("padding-bottom", heigthTitleService + 50);
        $(".services-block").css("margin-top", -heigthTitleService + (-30));

        if ($(window).width() < 768) {
            $(".section-header").css("padding-bottom", heigthTitleService + 130);
            $(".services-block").css("margin-top", -heigthTitleService + (-110));
        }

    }

    function ShowCircleButton(){

        $('.hover1 .g-service-block').delay(6000).css({
            'display': 'block'
        });
        $('.hover2 .g-service-block').delay(6300).css({
            'display': 'block'
        });
        $('.hover3 .g-service-block').delay(6600).css({
            'display': 'block'
        });
        $('.hover4 .g-service-block').delay(6900).css({
            'display': 'block'
        });
        $('.hover5 .g-service-block').delay(7200).css({
            'display': 'block'
        });
        $('.hover6 .g-service-block').delay(7500).css({
            'display': 'block'
        });
    }

    $(window)
        .on('load', function () {
            changeHeightHome();
            changeWowDelay("description-main", "4", "1");
            changeWowDelay("services-box", "5", "1");
            if($(window).scrollTop() === 0 || $(window).scrollTop() < $("#wr-section").innerHeight()) {
                ShowCircleButton();
                wow.init();
            }
            else {
                $("#wr-section div").removeClass("wow, animated");
                $("#wr-section svg").removeClass("wow, animated");
            }
        });

    $(window).resize(function() {
        changeHeightHome();
        ShowCircleButton();
        changeWowDelay("description-main", "4", "1");
        changeWowDelay("services-box", "5", "1");
        clearTimeout(window.resizedFinished);
        window.resizedFinished = setTimeout(function(){
            $('.wow, .animated').css({
                'animation-name': 'none'
            }).removeClass('animated');
        }, 250);
    });

    $(document).ready(function() {

        $('.section-header, header, .scroll-fix-block, .services-block').mousemove(function(event) {

            windowWidth = $(window).width();
            windowHeight = $(window).height();

            mouseXpercentage = Math.round(event.pageX / windowWidth * 100);
            mouseYpercentage = Math.round(event.pageY / windowHeight * 100);

            $('.section-header').css('background', 'radial-gradient(at ' + mouseXpercentage + '% ' + mouseYpercentage + '%, #043659, #07192d)');

        }).mouseleave(function() {

            $('.section-header').css('background', 'radial-gradient(at center, #043659, #07192d)');

        });


        $(".g-service-block").mouseenter(function() {
            if ($(window).width() < 768) {
                var btnWrap2 = $(this).children().eq(1);
                btnWrap2.css("visibility", "visible");
            }

            var btnWrap2 = $(this).children().eq(2),
                widthbtn = btnWrap2.children().innerWidth(),
                widthbtnpx = widthbtn + 60,
                btn_rect = $(this).children().eq(0);


            btn_rect.is(":hover") ? btnWrap2.children().css("visibility", "visible") : btnWrap2.children().css("visibility", "hidden");

            btnWrap2.css("width", widthbtnpx);
            $(this).siblings(".red").css("fill", "#A92E5C");
            btnWrap2.children().css("visibility", "visible");


        }).mouseleave(function() {
            if ($(window).width() < 768) {
                var btnWrap2 = $(this).children().eq(1);
                btnWrap2.css("visibility", "hidden");
            }
            var btnWrap2 = $(this).children().eq(2);

            btnWrap2.children().css("visibility", "hidden");
            btnWrap2.css("width", 0);
            $(this).siblings(".red").css("fill", "none");


        });

    });



})(jQuery);
