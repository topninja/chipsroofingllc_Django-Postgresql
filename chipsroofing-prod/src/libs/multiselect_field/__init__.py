"""
    Поле, которое может принимать набор значений из фиксированного списка
    choices. Значения в БД разделяются запятыми.

    Пример:
        class SomeModel(models.Model):
            LANGUAGES = (
                ('en', _('English')),
                ('ru', _('Russian')),
                ('ja', _('Japanese')),
                ('it', _('Italian')),
            )

            langs = MultiSelectField(_('langs'), choices=LANGUAGES, coerce=str, blank=True)

    Пример значения в модели:
        > instance.langs
        ('en', 'ja')

        > instance_empty.langs
        ()

"""
