import os
import re
import mimetypes
from bs4 import BeautifulSoup as Soup
from django.conf import settings
from django.template import loader
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

re_newline_spaces = re.compile(r'[\r \t]*\n[\r \t]*')
re_newlines = re.compile(r'\n{3,}')


def send(receivers, subject, message, from_email=None, attachments=None,
        host=None, port=None, username=None, password=None,
        use_tls=None, use_ssl=None, fail_silently=False):
    """
        Базовый метод отправки email.
        Позволяет явно указать учетную запись, от имени которой будет отправлено письмо,
        а также прикрепить к письму файлы.

        Параметр attachments - список, содержащий
            а) кортежи (ИМЯ_ФАЙЛА, СОДЕРЖИМОЕ_ФАЙЛА, [MIMETYPE])
            б) полные пути к файлам
    """
    if not receivers:
        return True

    if isinstance(receivers, str):
        receivers = [receivers]

    # создание текстовой альтернативы HTML-письма
    plain_message = strip_tags(message)
    plain_message = re_newline_spaces.sub('\n', plain_message)
    plain_message = re_newlines.sub('\n\n', plain_message)

    connection = get_connection(
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls,
        use_ssl=use_ssl,
        fail_silently=fail_silently
    )

    mail = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=receivers,
        attachments=None,
        connection=connection
    )
    mail.attach_alternative(message, 'text/html')

    if attachments is not None:
        for attachment in attachments:
            if isinstance(attachment, str):
                # TODO: см баг https://code.djangoproject.com/ticket/24623
                filename = os.path.basename(attachment)
                mimetype, _ = mimetypes.guess_type(filename)
                basetype, subtype = mimetype.split('/')
                readmode = 'r' if basetype == 'text' else 'rb'
                with open(attachment, readmode) as f:
                    content = f.read()
                mail.attach(filename, content, mimetype)
            else:
                filename, *other = attachment
                filename = os.path.basename(filename)
                mail.attach(filename, *other)

    return mail.send()


def send_template(request, receivers, subject, template, context=None, **kwargs):
    """
        Рендеринг письма из HTML-шаблона и его отправка.
    """
    site = get_current_site(request)

    # Вставка домена в тему письма
    subject = subject.format(domain=site.domain)

    # Рендеринг шаблона
    context = context or {}
    context.setdefault('domain', site.domain)
    message = loader.get_template(template).render(context, request=request)

    return send(receivers, subject, message, **kwargs)


# TODO: либо удалить отсюда, либо создать package и вынести в utils
def absolute_links(html, scheme='//', request=None):
    """
        1. Все ссылки становятся абсолютными с target=_blank.
        2. Ко всем таблицам добавляются аттрибуты cellpadding, cellspacing и border
    """
    site = get_current_site(request)

    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        href = tag.get('href')
        if not href:
            continue

        tag['target'] = '_blank'
        if href.startswith('//'):
            tag['href'] = '%s%s' % (scheme, href[2:])
        elif href.startswith('/'):
            tag['href'] = '%s%s%s' % (scheme, site.domain, href)

    for tag in soup.findAll('img'):
        if tag.has_attr('height'):
            del tag['height']

        src = tag.get('src')
        if not src:
            continue

        if src.startswith('//'):
            tag['src'] = '%s%s' % (scheme, src[2:])
        elif src.startswith('/'):
            tag['src'] = '%s%s%s' % (scheme, site.domain, src)

        # srcset
        srcset = tag.get('srcset')
        if not srcset:
            continue

        srcset_final = []
        for srcset_part in srcset.split(','):
            url, width = srcset_part.strip().split()
            if url.startswith('//'):
                url = '%s%s' % (scheme, url[2:])
            elif src.startswith('/'):
                url = '%s%s%s' % (scheme, site.domain, url)
            srcset_final.append('%s %s' % (url, width))
        tag['srcset'] = ','.join(srcset_final)

    # Добавление аттрибутов к таблицам
    for tag in soup.findAll('table'):
        for attr in ('border', 'cellpadding', 'cellspacing'):
            if not tag.has_attr(attr):
                tag[attr] = '0'

    return soup.decode_contents()
