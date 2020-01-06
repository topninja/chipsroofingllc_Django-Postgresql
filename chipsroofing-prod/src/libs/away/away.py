from urllib import parse
from bs4 import BeautifulSoup as Soup
from django.shortcuts import resolve_url
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


def is_same_domain(host, pattern):
    if not pattern:
        return False

    pattern = pattern.lower()
    return (
        pattern[0] == '.' and (host.endswith(pattern) or host == pattern[1:]) or
        pattern == host
    )


def away_links(request, html):
    """
        Заменяет все внешние ссылки в html-коде на единую точку с редиректом
    """
    site = get_current_site(request)
    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        if tag.get('href'):
            parsed = parse.urlparse(tag['href'])
            if '' not in (parsed.scheme, parsed.netloc) and not is_same_domain(parsed.netloc, site.domain):
                url = parsed.geturl()
                encoded_url = urlsafe_base64_encode(url.encode())
                tag['target'] = '_blank'
                tag['href'] = resolve_url('away') + '?url=' + encoded_url.decode()
                if tag.string:
                    tag.string = parse.unquote(tag.string)

    return soup.body.decode_contents()
