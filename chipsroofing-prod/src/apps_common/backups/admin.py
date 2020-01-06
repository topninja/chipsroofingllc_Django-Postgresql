import os
from functools import update_wrapper
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.core.management import call_command
from libs.download import AttachmentResponse
from .models import Backup


def _filesize(file):
    """ Получение размера файла """
    stat = os.stat(file)
    return stat.st_size


@admin.register(Backup)
class BackupDummyAdmin(admin.ModelAdmin):
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            url(r'^$', wrap(self.changelist), name='%s_%s_changelist' % info),
            url(r'^create/$', wrap(self.create), name='%s_%s_create' % info),
            url(r'^delete/(?P<filename>[\d_]+)/$', wrap(self.delete), name='%s_%s_delete' % info),
            url(r'^download/(?P<filename>[\d_]+)/$', wrap(self.download), name='%s_%s_download' % info),
        ]
        return urls

    @staticmethod
    def changelist(request):
        """ Список бэкапов """
        if not request.user.is_superuser:
            raise PermissionDenied

        if not os.path.isdir(settings.BACKUP_ROOT):
            os.mkdir(settings.BACKUP_ROOT, 0o755)

        zip_archives = []
        for file in reversed(sorted(os.listdir(settings.BACKUP_ROOT))):
            absfile = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))
            if os.path.isfile(absfile) and absfile.endswith('.zip'):
                zip_archives.append((
                    os.path.splitext(file)[0], _filesize(absfile)
                ))

        return render(request, 'backups/admin/index.html', {
            'files': zip_archives,
        })

    def create(self, request):
        """ Создание бэкапа """
        if not request.user.is_superuser:
            raise PermissionDenied

        call_command('zipdata')
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def delete(self, request, filename):
        """ Удаление бэкапа """
        if not request.user.is_superuser:
            raise PermissionDenied

        file = '{}.zip'.format(os.path.basename(filename))
        file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

        if os.path.isfile(file) and file.endswith('.zip'):
            os.unlink(file)

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def download(self, request, filename):
        """ Скачаивание бэкапа """
        if not request.user.is_superuser:
            raise PermissionDenied

        file = '{}.zip'.format(os.path.basename(filename))
        file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

        if os.path.isfile(file) and file.endswith('.zip'):
            return AttachmentResponse(request, file)

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)
