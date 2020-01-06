"""
    Всплывающий баннер.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'facebook_banner',
                ...
            )

        urls.py:
            ...
            url(r'^facebook_banner/', include('facebook_banner.urls', namespace='facebook_banner')),
            ...

        layout.html:
            <script>
                (function(d, s, id) {
                  var js, fjs = d.getElementsByTagName(s)[0];
                  if (d.getElementById(id)) return;
                  js = d.createElement(s); js.id = id;
                  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1915461638734808";
                  fjs.parentNode.insertBefore(js, fjs);
                }(document, 'script', 'facebook-jssdk'));
            </script>
"""

default_app_config = 'facebook_banner.apps.Config'
