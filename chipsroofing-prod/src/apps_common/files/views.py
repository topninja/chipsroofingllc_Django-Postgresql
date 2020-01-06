from django.db import models
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from libs.download import AttachmentResponse
from .models import PageFile


@never_cache
def download(request, file_id):
    page_file = get_object_or_404(PageFile, pk=file_id)
    PageFile.objects.filter(pk=page_file.pk).update(downloads=models.F('downloads')+1)
    return AttachmentResponse(request, page_file.file)
