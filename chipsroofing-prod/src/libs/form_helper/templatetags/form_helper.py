from collections import Iterable
from django.template import Library, loader

register = Library()


def format_classes(classes):
    """
        Приведение классов в единый вид списка.
    """
    if not classes:
        return []
    elif isinstance(classes, str):
        return classes.split()
    elif isinstance(classes, Iterable):
        return list(classes)
    else:
        return []


@register.simple_tag(takes_context=True)
def render_field(context, form, fieldname, template=None, classes=None, help_text=None, **kwargs):
    """
        Рендеринг одного поля формы.

        Пример:
            {% render_field form 'name' classes='blue-field big-field' %}
    """
    request = context.get('request')
    if not request:
        return ''

    field = form[fieldname]
    fieldclass_prefix = getattr(form, 'fieldclass_prefix', 'field')
    field_template = getattr(form, 'default_field_template', 'form_helper/field.html')
    field_classes = ['field', '%s-%s' % (fieldclass_prefix, fieldname)]
    field_errors = []
    field_context = {}

    # класс поля с префиксом формы
    if hasattr(form, 'get_field_fullname'):
        field_classes.append(form.get_field_fullname(fieldname))

    # класс для обязательного поля
    if field.field.required:
        required_css_class = getattr(form, 'required_css_class', 'required')
        if required_css_class:
            field_classes.append(required_css_class)

    # классы для неверно заполненного поля
    if form.is_bound and form._errors and fieldname in form._errors:
        field_errors.extend(field.errors)
        invalid_css_class = getattr(form, 'invalid_css_class', 'invalid')
        if invalid_css_class:
            field_classes.append(invalid_css_class)

    # Получаем данные из словаря field_templates
    custom_classes = []
    field_templates = getattr(form, 'field_templates', None)
    if field_templates:
        field_params = field_templates.get(fieldname)
        if isinstance(field_params, str):
            field_params = {
                'template': field_params,
            }
        if isinstance(field_params, dict):
            params = field_params.copy()
            field_template = params.pop('template')
            custom_classes = params.pop('classes', None)
            field_context.update(**params)

    # Установка дополнительных классов.
    # Либо из параметров функции, либо из field_templates.
    if classes:
        field_classes.extend(format_classes(classes))
    elif custom_classes:
        field_classes.extend(format_classes(custom_classes))

    # форсируем скрытый виджет для скрытого поля
    if field.is_hidden:
        hidden_template = getattr(form, 'hidden_field_template', None)
        if hidden_template:
            field_template = hidden_template

    # шаблон из параметра функции
    if template:
        field_template = template

    if help_text is None:
        help_text = field.help_text

    # Контекст рендеринга поля
    field_context.update(**kwargs)
    field_context.update(
        form=form,
        field=field,
        classes=' '.join(field_classes),
        errors=field_errors,
        help_text=help_text,
        render_help_text=getattr(form, 'render_help_text', False),
        render_errors=getattr(form, 'render_error_message', False),
    )
    return loader.get_template(field_template).render(field_context, request)


@register.simple_tag(takes_context=True)
def render_form(context, form, template=None):
    """
        Рендеринг формы.

        Пример:
            {% render_form form %}
    """
    template = template or 'form_helper/form.html'
    return loader.get_template(template).render({
        'form': form,
    }, context.get('request'))
