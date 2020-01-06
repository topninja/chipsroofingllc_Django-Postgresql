from urllib import parse
from django.contrib import admin
from django.shortcuts import redirect
from django.http.response import Http404
from django.contrib.contenttypes.models import ContentType
from libs.admin_utils import get_add_url, get_change_url, get_delete_url


def add_query(request, url):
    parsed = parse.urlparse(url)
    query = filter(bool, (parsed.query, request.GET.urlencode()))
    parsed = parsed._replace(
        query='&'.join(query)
    )
    return parsed.geturl()


@admin.site.admin_view
def add_related(request, content_type_id):
    try:
        ct = ContentType.objects.get(pk=content_type_id)
    except ContentType.DoesNotExist:
        raise Http404

    url = get_add_url(ct.app_label, ct.model)
    return redirect(add_query(request, url))


@admin.site.admin_view
def change_related(request, content_type_id, pk):
    try:
        ct = ContentType.objects.get(pk=content_type_id)
    except ContentType.DoesNotExist:
        raise Http404

    url = get_change_url(ct.app_label, ct.model, pk)
    return redirect(add_query(request, url))


@admin.site.admin_view
def delete_related(request, content_type_id, pk):
    try:
        ct = ContentType.objects.get(pk=content_type_id)
    except ContentType.DoesNotExist:
        raise Http404

    url = get_delete_url(ct.app_label, ct.model, pk)
    return redirect(add_query(request, url))
