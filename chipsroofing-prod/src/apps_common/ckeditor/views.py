from django.shortcuts import get_object_or_404
from libs.download import AttachmentResponse
from .models import PageFile


def download_pagefile(request, file_id):
    page_file = get_object_or_404(PageFile, pk=file_id)
    return AttachmentResponse(request, page_file.file)
