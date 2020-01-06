(function() {

    var loadJS = function(src, async) {
        var script = document.createElement('script');
        script.src = src;
        script.async = async || false;
        document.body.appendChild(script);
    };

    // for picturefill
    document.createElement("picture");
    if (!Modernizr.sizes || !Modernizr.srcset || !Modernizr.picture) {
        loadJS("/static/polyfills/picturefill.min.js");
    }

    if (!Modernizr.svg) {
        loadJS("/static/polyfills/svg2png.js");
    }
})();