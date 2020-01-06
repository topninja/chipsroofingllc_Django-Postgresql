"""
    Модуль, помогающй рендерить форму.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.form_helper',
                ...
            )

    Каждому полю даются два/три CSS-класса:
        1) field
            Это общий класс для всех полей

        2) field-NAME
            где NAME - имя поля в форме.

        3) field-FORM_PREFIX-NAME
            где FORM_PREFIX - префикс формы, а NAME - имя поля в форме.
            Если префикса у формы нет - этот класс не будет добавлен.

    Для полей типа radio и checkbox можно использовать встроенный шаблон
    form_helper/boolean_field.html, чтобы работала CSS-стилизация.

    Пример:
        forms.py:
            from django import forms
            from libs.form_helper.forms import FormHelperMixin

            class MyForm(FormHelperMixin, forms.Form):
                field_templates = {
                    'first_name': 'form_helper/unlabeled_field.html',
                    'last_name': {
                        'template': 'form_helper/unlabeled_field.html',
                        'param': 'value',
                    },
                }
                default_field_template = 'form_helper/unlabeled_field.html'

                ...

        template.html:
            {% load form_helper %}
            ...
            <form action="" method="post">
                {% render_form form %}

                <input type="submit" value="Submit">
            </form>

        template2.html:
            {% load form_helper %}
            ...
            <form action="" method="post">
                {% csrf_token %}

                {% render_field form 'name' %}
                {% render_field form 'age' param='value' template='fields/age_field.html' %}

                <input type="submit" value="Submit">
            </form>


    Пример обработки ошибок через JS:
        view.py:
            def form_validate(request):
                ...
                if not form.is_valid():
                    return JsonResponse({
                        'errors': form.error_dict,
                    })

        script.js:
            $form.on('submit', function() {
                $.ajax({
                    ...
                    success: function(response) {
                        response.errors.forEach(function(record) {
                            var $field = $form.find('.' + record.fullname);
                            $field.addClass(record.class);
                        })
                    }
                });

                return false;
            })

"""
