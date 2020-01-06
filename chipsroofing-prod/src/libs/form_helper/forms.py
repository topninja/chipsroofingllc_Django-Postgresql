from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


class PlainErrorList(ErrorList):
    def __str__(self):
        return ', '.join(str(error_message) for error_message in self)


class FormHelperMixin:
    """
        Миксина для форм, добавляющая

        1) метод для возбужения ошибки с указанным кодом:
            form.add_field_error('field1', 'required')

        2) ошибки в виде словарей (для JS):
            2.1) form.error_dict
            2.2) form.error_dict_full
    """

    # Выводить ли CSRF-токен
    csrf_token = True

    # Префикс классов поля
    fieldclass_prefix = 'field'

    # Класс, добавляемый полю, если оно заполнено некорректно
    invalid_css_class = 'invalid'

    # Класс, добавляемый полю, если оно обязательно
    required_css_class = 'required'

    # Выводить подписи к полям
    render_help_text = False

    # Выводить текстовые описания ошибок полей
    render_error_message = False

    # Шаблоны полей формы по их именам. В качестве значения
    # может быть строка с путем к файлу шаблона или словарь.
    # В случае словаря, путь к шаблону должен находиться
    # по ключу template. Дополнительные CSS-классы для поля
    # могут находиться по ключу classes. Остальные значения будут добавлены в контекст,
    # с которым будет рендериться этот шаблон.
    # Пример:
    #   field_templates = {
    #       'template': 'form_helper/field.html',
    #       'classes': 'red-field bold-text',
    #       'param': 'value',
    #   }
    field_templates = {}

    # Шаблоны полей по-умолчанию
    default_field_template = 'form_helper/field.html'
    hidden_field_template = 'form_helper/hidden_field.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = PlainErrorList

    def add_field_error(self, fieldname, code, params=None):
        """
            Возбуждает ошибку валидации в поле fieldname с кодом code
        """
        field = self.fields[fieldname]
        if code in field.error_messages:
            self.add_error(fieldname, ValidationError(
                field.error_messages[code],
                code=code,
                params=params
            ))
        elif hasattr(self, 'error_messages') and code in self.error_messages:
            self.add_error(fieldname, ValidationError(
                self.error_messages[code],
                code=code,
                params=params
            ))
        else:
            raise ValueError('Unknown code %r' % code)

    def get_field_fullname(self, fieldname):
        parts = (self.fieldclass_prefix, self.prefix, fieldname)
        parts = filter(bool, parts)
        parts = map(str, parts)
        return '-'.join(parts)

    def _field_errors(self):
        return tuple(
            (fieldname, self.errors[fieldname])
            for fieldname in self.fields
            if fieldname in self.errors
        )

    @property
    def error_dict(self):
        """
            Ошибки полей формы в виде кортежа словарей (в порядке следования полей в форме):

            (
                {
                    'name': 'field1',
                    'fullname': 'field-formprefix-field1',
                    'class: 'invalid',
                    'errors': [field_error1, field_error2, ...]
                },
                ...
            )
        """
        return tuple({
            'name': name,
            'fullname': self.get_field_fullname(name),
            'class': self.invalid_css_class,
            'errors': messages,
        } for name, messages in self._field_errors())

    @property
    def error_dict_full(self):
        """
            Аналогичен error_dict, но дополнительно включает
            ошибки всей формы.
        """
        errors = self.error_dict
        if NON_FIELD_ERRORS in self.errors:
            errors = ({
                'name': NON_FIELD_ERRORS,
                'fullname': NON_FIELD_ERRORS,
                'class': '',
                'errors': self.errors[NON_FIELD_ERRORS],
            }, ) + errors

        return errors
