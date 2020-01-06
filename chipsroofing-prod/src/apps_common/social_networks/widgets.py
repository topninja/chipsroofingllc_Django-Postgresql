from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, smart_urlquote


class TokenButtonWidget(forms.Widget):
    def __init__(self, text='', attrs=None):
        super().__init__(attrs=attrs)
        self.text = str(text)
        self.attrs.setdefault('target', '_self')
        self.attrs.setdefault('class', 'btn btn-info')

    def render(self, name, value, attrs=None):
        if value is None:
            return format_html(
                '<p class="text-error">{text}</p>',
                text=_('Populate form fields above'),
            )

        final_attrs = self.build_attrs(attrs)
        href = smart_urlquote(value)
        text = self.text or href
        return format_html(
            '<p><a href="{href}" {attrs}>{text}</a></p>',
            href=href,
            attrs=flatatt(final_attrs),
            text=force_str(text),
        )
