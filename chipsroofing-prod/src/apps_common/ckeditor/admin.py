import os
import mimetypes
from django.apps import apps
from django.contrib import admin
from django.forms.utils import flatatt
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.http import JsonResponse, Http404, HttpResponse
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from .models import PagePhoto, PageFile, SimplePhoto


def pagephoto_tag(instance, nocache=False):
    attrs = flatatt({
        'src': instance.photo.normal.url_nocache if nocache else instance.photo.normal.url,
        'srcset': ', '.join((
            instance.photo.wide.srcset_nocache,
            instance.photo.normal.srcset_nocache,
            instance.photo.mobile.srcset_nocache
        )),
        'width': instance.photo.wide.width,
        'height': instance.photo.wide.height,
        'sizes': '100vw',
        'data-id': instance.id,
        'data-source': instance.photo.url_nocache,
        'data-crop': instance.photo.croparea,
    })

    return """<img alt="" {attrs}>""".format(
        attrs=attrs,
    )


@admin.site.admin_view
def upload_pagephoto(request):
    """
        Функция, принимающая файлы, загружаемые через CKEditor.
        Может вызываться несколько раз для одного файла, если он разбит на части.
    """
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    field_name = request.GET.get('field_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        uploaded_file = upload_chunked_file(request, 'image')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    pagephoto = PagePhoto(
        app_name=app_label,
        model_name=model_name,
    )
    pagephoto.photo.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        pagephoto.full_clean()
    except ValidationError as e:
        pagephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        pagephoto.save()

    return JsonResponse({
        'tag': pagephoto_tag(pagephoto),
        'field': field_name,
        'id': pagephoto.pk,
    })


@admin.site.admin_view
def rotate_pagephoto(request):
    photo_id = request.GET.get('id')
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    direction = request.GET.get('direction')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        pagephoto = PagePhoto.objects.get(
            id=photo_id,
            app_name=app_label,
            model_name=model_name,
        )
    except PagePhoto.DoesNotExist:
        raise Http404

    if direction == 'left':
        pagephoto.photo.rotate(-90)
    else:
        pagephoto.photo.rotate(90)

    return JsonResponse({
        'tag': pagephoto_tag(pagephoto, nocache=True),
    })


@admin.site.admin_view
def crop_pagephoto(request):
    photo_id = request.GET.get('id')
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        pagephoto = PagePhoto.objects.get(
            id=photo_id,
            app_name=app_label,
            model_name=model_name,
        )
    except PagePhoto.DoesNotExist:
        raise Http404

    try:
        croparea = request.GET.get('croparea', '')
        pagephoto.photo.recut(croparea=croparea)
    except ValueError:
        raise Http404

    return JsonResponse({
        'tag': pagephoto_tag(pagephoto, nocache=True),
    })


def pagefile_tag(instance, classes=''):
    return """
        <div class="page-file {classes}" data-id="{id}">
            <a href="{url}">
                <span>{display}</span>
            </a>
        </div>
    """.format(
        id=instance.id,
        classes=classes,
        url=reverse('ckeditor:download_pagefile', kwargs={
            'file_id': instance.pk,
        }),
        display=os.path.splitext(instance.file.name)[0],
    )


@admin.site.admin_view
def upload_pagefile(request):
    """
        Функция, принимающая файлы, загружаемые через CKEditor.
        Может вызываться несколько раз для одного файла, если он разбит на части.
    """
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    field_name = request.GET.get('field_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        uploaded_file = upload_chunked_file(request, 'file')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    pagefile = PageFile(
        app_name=app_label,
        model_name=model_name,
    )
    pagefile.file.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        pagefile.full_clean()
    except ValidationError as e:
        pagefile.file.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        pagefile.save()

    # Определяем тип файла
    mimetype, encoding = mimetypes.guess_type(pagefile.file.path)
    classes = PageFile.MIME_CLASSES.get(mimetype, '')

    return JsonResponse({
        'tag': pagefile_tag(pagefile, classes=classes),
        'field': field_name,
        'id': pagefile.pk,
    })


def simplephoto_tag(instance, nocache=False):
    attrs = flatatt({
        'src': instance.photo.url_nocache if nocache else instance.photo.url,
        'srcset': ', '.join((
            instance.photo.srcset_nocache,
            instance.photo.mobile.srcset_nocache
        )),
        'width': instance.photo.width,
        'height': instance.photo.height,
        'sizes': '100vw',
    })

    return """<img data-id="{id}" alt="" {attrs}>""".format(
        id=instance.id,
        attrs=attrs,
    )


@admin.site.admin_view
def upload_simplephoto(request):
    """
        Функция, принимающая файлы, загружаемые через CKEditor.
        Может вызываться несколько раз для одного файла, если он разбит на части.
    """
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    field_name = request.GET.get('field_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        uploaded_file = upload_chunked_file(request, 'image')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    simplephoto = SimplePhoto(
        app_name=app_label,
        model_name=model_name,
    )
    simplephoto.photo.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        simplephoto.full_clean()
    except ValidationError as e:
        simplephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        simplephoto.save()

    return JsonResponse({
        'tag': simplephoto_tag(simplephoto),
        'field': field_name,
        'id': simplephoto.pk,
    })
