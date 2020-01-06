"""
    Модуль, расставляющий заглушки для блоков, которые будут подгружены через AJAX.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'placeholder',
                ...
            )

            PIPELINE = {
                ...
                'placeholder/js/placeholder.js',
                ...
            }

        urls.py:
            ...
            url(r'^placeholder/', include('placeholder.urls', namespace='placeholder')),
            ...

    1) Помимо имени в {% placeholder %} можно указывать любое кол-во дополнительных
       параметров, которые должны быть сериализуемы, т.к. они превращаются в data-атрибуты
       тэга заглушки
    2) Заглушка с одним именем может встречаться на странице несколько раз с разными параметрами.
       Каждое такое появление называется "часть заглушки".
    3) На каждое имя регистрируется функция-обработчик, которая должна вернуть
       одну или несколько отрендеренных частей в виде итератора
    4) Функция должна быть зарегистрирована в apps.py

    Пример:
        # apps.py:
            def ready(self):
                from placeholder.utils import register_placeholder
                from .views_ajax import contact_placeholder
                register_placeholder('contact_block', contact_placeholder)

        # views.py:
            def contact_part(request, **params):
                bg = params.get('bg', 'yellow')
                if not bg:
                    return ''

                title = params.get('bg', 'Join us')
                return loader.render_to_string('contact_block/part.html', {
                    'bg': bg,
                    'title': title,
                }, request=request)

            def contact_placeholder(request, name, parts):
                return [contact_part(request, **part_params) for part_params in parts]


        # template.html:
            {% load placeholder %}

            {% placeholder "contact_block" bg="red" %}
            {% placeholder "contact_block" bg="blue" title="Hello" %}

"""

default_app_config = 'placeholder.apps.Config'
