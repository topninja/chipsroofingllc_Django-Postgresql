(function(l,q,C){function y(b){return b.replace(/^\s+|\s+$/g,"")}function D(b,a){var d,c=0;if(!b||!a)return!1;for(;d=a[c++];)if(b===d)return!0;return!1}function t(b){var a=0,d;for(this._rules=[];d=b[a++];)this._rules.push(new z(d))}function z(b){this._rule=b}function f(b){if(!(this instanceof f))return new f(b);this._options=b;b.keywords||(this._options={keywords:b});this._promise=[];this._getStylesheets();this._downloadStylesheets();this._parseStylesheets();this._filterCSSByKeywords();this._buildMediaQueryMap();
this._reportInitialMatches();this._addMediaListeners()}C=RegExp("^"+String({}.valueOf).replace(/[.*+?\^${}()|\[\]\\]/g,"\\$&").replace(/valueOf|for [^\]]+/g,".+?")+"$");var E=function(){var b=q.getElementsByTagName("base")[0],a=/^([a-zA-Z:]*\/\/)/;return function(d){return!a.test(d)&&!b||d.replace(RegExp.$1,"").split("/")[0]===location.host}}(),G=l.matchMedia&&l.matchMedia("only all").matches,A=C.test(l.matchMedia),F=function(){function b(){if(0===g.readyState||4===g.readyState){var c;(c=k[0])&&a(c);
c||d()}}function a(a){h++;g.open("GET",a,!0);g.onreadystatechange=function(){4!=g.readyState||200!=g.status&&304!=g.status||(c[a]=g.responseText,k.shift(),b())};g.send(null)}function d(){for(var a;a=e.shift();){var b=a.urls;a=a.fn;for(var h=[],d=void 0,g=0;d=b[g++];)h.push(c[d]);a.call(null,h)}}var c={},k=[],e=[],h=0,g=function(){var a;try{a=new l.XMLHttpRequest}catch(c){a=new l.ActiveXObject("Microsoft.XMLHTTP")}return a}();return{request:function(a,h){e.push({urls:a,fn:h});for(var g,n=0,f=0;g=a[n++];)c[g]&&
f++;if(f===a.length)d();else{for(n=0;g=a[n++];)c[g]||D(g,k)||k.push(g);b()}},clearCache:function(){c={}},_getRequestCount:function(){return h}}}(),u={_cache:{},clearCache:function(){u._cache={}},parse:function(b,a){function d(){return e(/^\{\s*/)}function c(){return e(/^\}\s*/)}function k(){var a,c=[];e(/^\s*/);for(h(c);"}"!=b.charAt(0)&&(a=n()||t()||q()||v("import")||v("charset")||v("namespace")||r()||x());)c.push(a),h(c);return c}function e(a){if(a=a.exec(b))return b=b.slice(a[0].length),a}function h(a){a=
a||[];for(var c;c=g();)a.push(c);return a}function g(){if("/"==b[0]&&"*"==b[1]){for(var a=2;"*"!=b[a]||"/"!=b[a+1];)++a;var a=a+2,c=b.slice(2,a-2);b=b.slice(a);e(/^\s*/);return{comment:c}}}function f(){var a=e(/^([^{]+)/);if(a)return y(a[0]).split(/\s*,\s*/)}function m(){var a=e(/^(\*?[\-\w]+)\s*/);if(a&&(a=a[0],e(/^:\s*/))){var c=e(/^((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^\)]*?\)|[^};])+)\s*/);if(c)return c=y(c[0]),e(/^[;\s]*/),{property:a,value:c}}}function l(){for(var a,c=[];a=e(/^(from|to|\d+%|\.\d+%|\d+\.\d+%)\s*/);)c.push(a[1]),
e(/^,\s*/);if(c.length)return{values:c,declarations:w()}}function n(){var a=e(/^@([\-\w]+)?keyframes */);if(a){var b=a[1];if(a=e(/^([\-\w]+)\s*/))if(a=a[1],d()){h();for(var g,k=[];g=l();)k.push(g),h();if(c())return a={name:a,keyframes:k},b&&(a.vendor=b),a}}}function q(){var a=e(/^@supports *([^{]+)/);if(a&&(a=y(a[1]),d())){h();var b=k();if(c())return{supports:a,rules:b}}}function t(){var a=e(/^@media *([^{]+)/);if(a&&(a=y(a[1]),d())){h();var b=k();if(c())return{media:a,rules:b}}}function r(){if(e(/^@page */)){var a=
f()||[],b=[];if(d()){h();for(var g;g=m()||p();)b.push(g),h();if(c())return{type:"page",selectors:a,declarations:b}}}}function p(){var a=e(/^@([a-z\-]+) */);if(a)return{type:a[1],declarations:w()}}function v(a){var c=e(new RegExp("^@"+a+" *([^;\\n]+);\\s*"));if(c){var b={};b[a]=y(c[1]);return b}}function w(){var a=[];if(d()){h();for(var b;b=m();)a.push(b),h();if(c())return a}}function x(){var c=f();if(c)return h(),{selectors:c,declarations:w(),url:a}}if(a&&u._cache[a])return u._cache[a];b=b.replace(/\/\*[\s\S]*?\*\//g,
"");return u._cache[a]=k()},filter:function(b,a){function d(a,c){if(a||c)return a?a.concat(c):[c]}function c(a){null==a.media&&delete a.media;null==a.supports&&delete a.supports;e.push(a)}function k(b,e,f){for(var m,l=0;m=b[l++];)if(m.declarations){var n;n=m;var q=e,t=f;if(a.selectors){var r;b:{r=n.selectors.join(",");var p=a.selectors;if(p)for(var v=p.length;v--;)if(0<=r.indexOf(p[v])){r=!0;break b}r=void 0}r?(c({media:q,supports:t,selectors:n.selectors,declarations:n.declarations,url:n.url}),n=
!0):n=void 0}else n=void 0;if(!n)a:if(n=e,q=f,a.declarations)for(r=void 0,t=0;r=m.declarations[t++];){b:{for(var p=a.declarations,v=/\*/g,w=void 0,x=void 0,x=w=void 0,u=0;w=p[u++];)if(x=w.split(":"),w=new RegExp("^"+y(x[0]).replace(v,".*")+"$"),x=new RegExp("^"+y(x[1]).replace(v,".*")+"$"),w.test(r.property)&&x.test(r.value)){r=!0;break b}r=void 0}if(r){c({media:n,supports:q,selectors:m.selectors,declarations:m.declarations,url:m.url});break a}}}else m.rules&&m.media?k(m.rules,d(e,m.media),f):m.rules&&
m.supports&&k(m.rules,e,d(f,m.supports))}var e=[];k(b);return e}},p=function(){function b(){if(c)return c;var a=q.documentElement,b=q.body,d=a.style.fontSize,k=b.style.fontSize,f=q.createElement("div");a.style.fontSize="1em";b.style.fontSize="1em";b.appendChild(f);f.style.width="1em";f.style.position="absolute";c=f.offsetWidth;b.removeChild(f);b.style.fontSize=k;a.style.fontSize=d;return c}var a=/\(min\-width:[\s]*([\s]*[0-9\.]+)(px|em)[\s]*\)/,d=/\(max\-width:[\s]*([\s]*[0-9\.]+)(px|em)[\s]*\)/,
c,k;return{matchMedia:function(c){if(G)c=l.matchMedia(c);else{var h,g,f=!1;k=q.documentElement.clientWidth;a.test(c)&&(h="em"===RegExp.$2?parseFloat(RegExp.$1)*b():parseFloat(RegExp.$1));d.test(c)&&(g="em"===RegExp.$2?parseFloat(RegExp.$1)*b():parseFloat(RegExp.$1));h&&g?f=h<=k&&g>=k:(h&&h<=k&&(f=!0),g&&g>=k&&(f=!0));c={matches:f,media:c}}return c},clearCache:function(){A||(k=null)}}}(),B=function(){function b(a,b){var e;return function(){clearTimeout(e);e=setTimeout(a,b)}}var a=function(){var a=
[];return{add:function(b,e,d){for(var g,f=0;g=a[f++];)if(g.polyfill==b&&g.mql===e&&g.fn===d)return!1;e.addListener(d);a.push({polyfill:b,mql:e,fn:d})},remove:function(b){for(var e,d=0;e=a[d++];)e.polyfill===b&&(e.mql.removeListener(e.fn),a.splice(--d,1))}}}(),d=function(a){function b(){for(var e,d=0;e=a[d++];)e.fn()}return{add:function(e,d){a.length||(l.addEventListener?l.addEventListener("resize",b,!1):l.attachEvent("onresize",b));a.push({polyfill:e,fn:d})},remove:function(d){for(var f,g=0;f=a[g++];)f.polyfill===
d&&a.splice(--g,1);a.length||(l.removeEventListener?l.removeEventListener("resize",b,!1):l.detachEvent&&l.detachEvent("onresize",b))}}}([]);return{removeListeners:function(b){A?a.remove(b):d.remove(b)},addListeners:function(c,f){var e=c._mediaQueryMap,h={};(function(){for(var a in e)e.hasOwnProperty(a)&&(h[a]=p.matchMedia(a).matches)})();(function(){if(A)for(var g in e)e.hasOwnProperty(g)&&function(b,d){a.add(c,b,function(){f.call(c,d,b.matches)})}(e[g],g);else g=b(function(a,b){return function(){var c,
d={};p.clearCache();for(c in b)b.hasOwnProperty(c)&&(d[c]=p.matchMedia(c).matches,d[c]!=h[c]&&f.call(a,c,p.matchMedia(c).matches));h=d}}(c,e),c._options.debounceTimeout||100),d.add(c,g)})()}}}();t.prototype.each=function(b,a){var d,c=0;for(a||(a=this);d=this._rules[c++];)b.call(a,d)};t.prototype.size=function(){return this._rules.length};t.prototype.at=function(b){return this._rules[b]};z.prototype.getDeclaration=function(){for(var b={},a=0,d,c=this._rule.declarations;d=c[a++];)b[d.property]=d.value;
return b};z.prototype.getSelectors=function(){return this._rule.selectors.join(", ")};z.prototype.getUrl=function(){return this._rule.url};z.prototype.getMedia=function(){return this._rule.media.join(" and ")};f.prototype.doMatched=function(b){this._doMatched=b;this._resolve();return this};f.prototype.undoUnmatched=function(b){this._undoUnmatched=b;this._resolve();return this};f.prototype.getCurrentMatches=function(){for(var b=0,a,d,c=[];a=this._filteredRules[b++];)(d=a.media&&a.media.join(" and "))&&
!p.matchMedia(d).matches||c.push(a);return new t(c)};f.prototype.destroy=function(){this._undoUnmatched&&(this._undoUnmatched(this.getCurrentMatches()),B.removeListeners(this))};f.prototype._defer=function(b,a){b.call(this)?a.call(this):this._promise.push({condition:b,callback:a})};f.prototype._resolve=function(){for(var b,a=0;b=this._promise[a];)b.condition.call(this)?(this._promise.splice(a,1),b.callback.call(this)):a++};f.prototype._getStylesheets=function(){var b=0,a,d,c,f,e=[];if(this._options.include)for(d=
this._options.include;a=d[b++];){if(c=q.getElementById(a))"STYLE"===c.nodeName?(a={text:c.textContent},e.push(a)):c.media&&"print"==c.media||!E(c.href)||(a={href:c.href},c.media&&(a.media=c.media),e.push(a))}else{d=this._options.exclude;for(f=q.getElementsByTagName("link");c=f[b++];)c.rel&&"stylesheet"==c.rel&&"print"!=c.media&&E(c.href)&&!D(c.id,d)&&(a={href:c.href},c.media&&(a.media=c.media),e.push(a));d=q.getElementsByTagName("style");for(b=0;a=d[b++];)a.textContent&&(a={text:a.textContent},e.push(a))}return this._stylesheets=
e};f.prototype._downloadStylesheets=function(){for(var b=this,a,d=[],c=0;a=this._stylesheets[c++];)d.push(a.href);F.request(d,function(a){for(var c,d=0;c=a[d];)b._stylesheets[d++].text=c;b._resolve()})};f.prototype._parseStylesheets=function(){this._defer(function(){return this._stylesheets&&this._stylesheets.length&&this._stylesheets[0].text},function(){for(var b=0,a;a=this._stylesheets[b++];)a.rules=u.parse(a.text,a.href)})};f.prototype._filterCSSByKeywords=function(){this._defer(function(){return this._stylesheets&&
this._stylesheets.length&&this._stylesheets[0].rules},function(){for(var b,a,d=[],c=0;b=this._stylesheets[c++];)(a=b.media)&&"all"!=a&&"screen"!=a?d.push({rules:b.rules,media:b.media}):d=d.concat(b.rules);this._filteredRules=u.filter(d,this._options.keywords)})};f.prototype._buildMediaQueryMap=function(){this._defer(function(){return this._filteredRules},function(){var b=0,a;for(this._mediaQueryMap={};a=this._filteredRules[b++];)a.media&&(a=a.media.join(" and "),this._mediaQueryMap[a]=p.matchMedia(a))})};
f.prototype._reportInitialMatches=function(){this._defer(function(){return this._filteredRules&&this._doMatched},function(){this._doMatched(this.getCurrentMatches())})};f.prototype._addMediaListeners=function(){this._defer(function(){return this._filteredRules&&this._doMatched&&this._undoUnmatched},function(){B.addListeners(this,function(b,a){for(var d=0,c,f=[],e=[];c=this._filteredRules[d++];)c.media&&c.media.join(" and ")==b&&(a?f:e).push(c);f.length&&this._doMatched(new t(f));e.length&&this._undoUnmatched(new t(e))})})};
f.modules={DownloadManager:F,StyleManager:u,MediaManager:p,EventManager:B};f.constructors={Ruleset:t,Rule:z};l.Polyfill=f})(window,document);


(function() {

    /*
        Полифилл, подменяющий в стилях "background" и "background-image"
        расширение ".svg" на ".png".
     */

    var background_url = /url\((.*\.svg)\)/i;
    var svg = /\.svg/i;


    // получение абсолютного пути по относительному
    var absolute = function(base, relative) {
        var stack = base.split("/"),
            parts = relative.split("/");

        if (parts[0] == '') {
            return relative
        }

        // remove current file name (or empty string)
        stack.pop();

        for (var i=0; i<parts.length; i++) {
            if (parts[i] == ".")
                continue;
            if (parts[i] == "..")
                stack.pop();
            else
                stack.push(parts[i]);
        }
        return stack.join("/");
    };


    function doMatched(rules) {
        var style_content = '';

        // добавление fallback-стиля в текст
        var add_new_style = function(selectors, new_url, base) {
            if (base) {
                new_url = absolute(base, new_url);
            }

            style_content += selectors + '{background-image: url(' + new_url + ');}\n';
        };

        // замена SVG на PNG
        rules.each(function(rule) {
            var declarations = rule.getDeclaration();
            var match, new_url;

            if ('background' in declarations) {
                match = background_url.exec(declarations['background']);
                if (match) {
                    new_url = match[1].replace(svg, '.png');
                    add_new_style(rule.getSelectors(), new_url, rule.getUrl());
                }
            } else if ('background-image' in declarations) {
                new_url = declarations['background-image'].replace(svg, '.png');
                add_new_style(rule.getSelectors(), new_url, rule.getUrl());
            }
        });

        // добавление тега style
        var head = document.head || document.getElementsByTagName('head')[0];
        var style = document.createElement('style');
        style.type = 'text/css';
        if (style.styleSheet){
          style.styleSheet.cssText = style_content;
        } else {
          style.appendChild(document.createTextNode(style_content));
        }
        head.appendChild(style);
    }

    Polyfill({
        declarations:["background-image:*\\.svg\\)", "background:*\\.svg\\)*"]
    }).doMatched(doMatched)

})();