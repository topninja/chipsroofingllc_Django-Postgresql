def get_form_field_value(form, fieldname, cleaned_data=None):
    """
        Получение значения поля формы.
    """
    field = form.fields[fieldname]
    if cleaned_data is not None:
        return cleaned_data.get(fieldname, field.initial)
    elif form.is_bound:
        return form.cleaned_data.get(fieldname, field.initial)
    else:
        return form.initial.get(fieldname, field.initial)


def require_fields(form, *fields):
    """
        Вызывает ошибку "required" на указанных полях, если они пусты.
        Используется совместно с blank=True.
    """
    if not form.is_bound:
        return

    data = form.cleaned_data
    for fieldname in fields:
        value = data.get(fieldname)
        field = form.fields[fieldname]
        if value in field.empty_values:
            form.add_field_error(fieldname, 'required')
