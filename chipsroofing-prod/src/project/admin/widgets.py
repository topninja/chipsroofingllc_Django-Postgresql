from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.html import format_html, smart_urlquote
from django.forms.utils import to_current_timezone
from suit.widgets import SuitDateWidget, HTML5Input, AutosizedTextarea as DefaultAutosizedTextarea


class LinkWidget(forms.Widget):
    """ Виджет простой ссылки """
    def __init__(self, text='', attrs=None):
        super().__init__(attrs=attrs)
        self.text = str(text)
        self.attrs.setdefault('target', '_self')

    def render(self, name, value, attrs=None):
        if value is None:
            return None

        final_attrs = self.build_attrs(attrs)
        href = smart_urlquote(value)
        text = self.text or href
        return format_html(
            '<a href="{href}" {attrs}>{text}</a>',
            href=href,
            attrs=flatatt(final_attrs),
            text=force_str(text),
        )


class URLWidget(forms.URLInput):
    """ Виджет URL """
    @staticmethod
    def append(value):
        if value:
            output = '<a href="{href}" class="add-on" target="_blank"><i class="icon-globe"></i></a>'
            href = force_str(value)
            return format_html(output, href=smart_urlquote(href))
        else:
            output = '<span class="add-on"><i class="icon-globe"></i></span>'
            return format_html(output)

    def render(self, name, value, attrs=None):
        html = super().render(name, value, attrs)
        return format_html(
            '<div class="url input-append">'
            '  {html} '
            '  {append}'
            '</div>',
            html=html,
            append=self.append(value)
        )


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    """ Виджет даты-времени """
    def __init__(self, attrs=None):
        subwidgets = (
            SuitDateWidget(attrs=attrs),
            HTML5Input(attrs={'class': 'input-small'}, input_type='time')
        )
        forms.MultiWidget.__init__(self, subwidgets, attrs)

    def format_output(self, rendered_widgets):
        return ' '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0, second=0)]
        return [None, None]


class AutosizedTextarea(DefaultAutosizedTextarea):
    """ Фикс бага раннего вызова, из-за которого высота не устанавливается при открытии страницы """
    def render(self, name, value, attrs=None):
        output = super(DefaultAutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">"
            "Suit.$(function(){ Suit.$('#id_%s').autosize(); })"
            "</script>"
            % name)
        return output

    def value_from_datadict(self, data, files, name):
        # FIX: некорректный подсчет длины при валидации
        default = super().value_from_datadict(data, files, name)
        return default.replace('\r\n', '\n')

