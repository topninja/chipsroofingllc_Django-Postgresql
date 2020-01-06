import re
from html import unescape
from bs4 import BeautifulSoup as Soup, NavigableString
from softhyphen.html import get_hyphenator_for_language, SOFT_HYPHEN
from django.core.cache import caches
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags, escape
from django.utils.translation import get_language
from django.template import Library, defaultfilters
from libs.description import description as description_func

register = Library()

re_nbsp = re.compile('(?<![\w’\'"])([\w’]{1,3})\s+')
re_clean_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')
re_not_numbers = re.compile('[^+\d]+')


def get_hybernator():
    lang = get_language()
    if lang == 'ru':
        lang = 'ru-RU'

    hybernator = get_hyphenator_for_language(lang)
    hybernator.left = 4
    hybernator.right = 3
    return hybernator


def hybernate_string(string):
    hybernator = get_hybernator()
    result = (
        hybernator.inserted(word, SOFT_HYPHEN)
        for word in string.split()
    )
    return ' '.join(result)


def process_tag(tag, valid_tags=()):
    if isinstance(tag, NavigableString):
        return tag

    if tag.name in valid_tags:
        for subtag in tag.contents:
            subtag.replaceWith(process_tag(subtag, valid_tags))
        return tag
    else:
        result = ""
        for subtag in tag.contents:
            result += str(process_tag(subtag, valid_tags))
        return result


@register.filter(is_safe=True, name="striptags_except")
def strip_tags_except_filter(html, args):
    """
        Удаление HTML-тэгов, кроме перечисленных в аргументе.

        Пример:
            {{ text|striptags_except:"a, p" }}
    """
    valid_tags = [item.strip() for item in args.split(',')]

    soup = Soup(html, 'html5lib')

    for tag in soup.body:
        tag.replaceWith(process_tag(tag, valid_tags))

    result = soup.body.decode_contents()
    return re_clean_newlines.sub('\n', result).replace('\xa0', '&nbsp;')


def _typograf_replace(text):
    last_pos = -1
    length = 1

    def sub_func(match):
        nonlocal last_pos, length
        value = match.group(1)

        if last_pos == match.start():
            length += 1
        else:
            length = 1

        if length == 2:
            return '%s ' % value

        last_pos = match.end()
        return '%s&nbsp;' % value

    return re_nbsp.sub(sub_func, text)


@register.filter(is_safe=True)
def typograf(html):
    """
        Удаление висячих предлогов
    """
    soup = Soup(html, 'html5lib')
    for tag in soup.findAll(text=True):
        if re_nbsp.search(tag):
            new_tag = soup.new_string(unescape(_typograf_replace(tag)))
            tag.replace_with(new_tag)

    return soup.body.decode_contents().replace('\xa0', '&nbsp;')


@register.filter(is_safe=True, needs_autoescape=True)
def linewraps(text, tagname='p', autoescape=True):
    """
        Разбивка текста на строки и оборачивание строк тэгом tagname.
        Пустые строки удаляются.
    """
    text = re_clean_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    text_lines = text.strip().split('\n')

    if autoescape:
        text_lines = map(escape, text_lines)

    result = '</{0}><{0}>'.format(tagname).join(text_lines)
    result = '<{0}>{1}</{0}>'.format(tagname, result)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def clean(html, autoescape=None):
    """
        Алиас для трех фильтров: striptags, linebreaksbr, typograf, safe
    """
    text = strip_tags(str(html))
    text = defaultfilters.linebreaksbr(text, autoescape=autoescape)
    text = typograf(text)
    return mark_safe(text)


@register.filter(is_safe=True)
def softhyphen(value):
    """
        Вставка невидимых переносов в слова
    """
    cache = caches['default']
    key = ':'.join(map(str, (value, get_language())))
    if key in cache:
        return cache.get(key)
    else:
        result = hybernate_string(value)
        cache.set(key, result, timeout=6*3600)
        return result


@register.filter(is_safe=True)
def description(value, args):
    minlen, maxlen = (int(item.strip()) for item in args.split(','))
    return description_func(value, minlen, maxlen)


@register.filter(is_safe=True)
def phone(value):
    """
        Оставляет только цифры и знак плюса
    """
    return re_not_numbers.sub('', value)


@register.filter(is_safe=True)
def unescape_html(html):
    return unescape(html)
