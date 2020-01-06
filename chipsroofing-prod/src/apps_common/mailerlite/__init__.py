"""
    Модуль подписки на рассылку.

    Зависит от:
        premailer
        libs.associative_request
        libs.color_field
        libs.pipeline
        libs.templatetags

    Установка:
        # settings.py:
            INSTALLED_APPS = (
                ...
                'mailerlite',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'mailerlite',
                    'icon': 'icon-envelope',
                    'models': (
                        'RegularCampaign',
                        'Subscriber',
                        'Group',
                        'MailerConfig',
                    )
                },
            }

            MAILERLITE_APIKEY = '438b16c79cbd9acea354a1c1ad5eda08'

        # urls.py:
            ...
            url(r'^mailerlite/', include('mailerlite.urls', namespace='mailerlite')),
            ...

        # crontab
            */30 * * * * . $HOME/.profile; ~/aor.com/env/bin/python3 ~/aor.com/src/manage.py mailerlite -eg -es -ec
            10 * * * * . $HOME/.profile; ~/aor.com/env/bin/python3 ~/aor.com/src/manage.py mailerlite -ig -is -ic


    Использование:
        # views.py:
            from mailerlite import SubscribeForm

            class IndexView(View):
                def get(self, request, *args, **kwargs):
                    ...
                    return self.render_to_response({
                        subscribe_form': SubscribeForm(),
                        ...
                    })

                def post(self, request, *args, **kwargs):
                    ...
                    email = form.cleaned_data.get('email')
                    subscriber = make_subscriber(email)
                    subscriber.groups.add(*groups)

        # template.html:
            <form action="{% url 'mailerlite:ajax_subscribe' %}" method="post" id="subscribe-form">
              {% render_form subscribe_form %}
              <input type="submit" value="Subscribe" class="btn">
            </form>

"""

default_app_config = 'mailerlite.apps.Config'
