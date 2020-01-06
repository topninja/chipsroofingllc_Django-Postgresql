import re
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from ...models import PagePhoto, PageFile, SimplePhoto

re_pagephoto = re.compile('/page_photos/\d+/photo_(\d+)')
re_pagefile = re.compile('/download_pagefile/(\d+)/')
re_simplephotos = re.compile('/simple_photos/\d+/photo_(\d+)')


class Command(BaseCommand):
    """
        Удаление фотографий, которые не привязаны к сущностям.

        pm clean_page_photos app.modelname note text
    """
    help = 'Removes unused PagePhoto and SimplePhoto instances'

    @staticmethod
    def get_model(modelpath):
        if isinstance(modelpath, str):
            return apps.get_model(*modelpath.rsplit('.', 1))

    @staticmethod
    def get_apps():
        return (
            app
            for app in apps.get_apps()
            if app.__file__.startswith(settings.BASE_DIR)
        )

    @staticmethod
    def get_model_textfields(model):
        return [
            item.name
            for item in model._meta.get_fields()
            if not item.auto_created and hasattr(item, 'get_internal_type') and item.get_internal_type() == 'TextField'
        ]

    def process_model(self, app, model):
        app = model._meta.app_label
        modelname = model._meta.model_name
        fields = self.get_model_textfields(model)
        if not fields:
            return

        self.stdout.write('Processing model %s.%s...' % (app, modelname))

        # Проверка загруженных, но отсутсвующих в тексте фотографий
        for instance in model.objects.all():
            used_pagephotos = []
            for fieldname in fields:
                field_value = getattr(instance, fieldname)
                matched_ids = re_pagephoto.findall(str(field_value))
                used_pagephotos.extend(matched_ids)

            used_pagefiles = []
            for fieldname in fields:
                field_value = getattr(instance, fieldname)
                matched_ids = re_pagefile.findall(str(field_value))
                used_pagefiles.extend(matched_ids)

            used_simplephotos = []
            for fieldname in fields:
                field_value = getattr(instance, fieldname)
                matched_ids = re_simplephotos.findall(str(field_value))
                used_simplephotos.extend(matched_ids)

            attached_unused_pagephotos = PagePhoto.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_pagephotos)
            if attached_unused_pagephotos:
                self.stdout.write('Deleted %s PagePhoto attached to %s (#%s)' % (
                    attached_unused_pagephotos.count(),
                    modelname,
                    instance.pk,
                ))
                attached_unused_pagephotos.delete()

            attached_unused_pagefiles = PageFile.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_pagefiles)
            if attached_unused_pagefiles:
                self.stdout.write('Deleted %s PageFile attached to %s (#%s)' % (
                    attached_unused_pagefiles.count(),
                    modelname,
                    instance.pk,
                ))
                attached_unused_pagefiles.delete()

            attached_unused_simplephotos = SimplePhoto.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_simplephotos)
            if attached_unused_simplephotos:
                self.stdout.write('Deleted %s SimplePhoto attached to %s (#%s)' % (
                    attached_unused_simplephotos.count(),
                    modelname,
                    instance.pk,
                ))
                attached_unused_simplephotos.delete()

    def handle(self, *args, **options):
        page_photos = PagePhoto.objects.filter(instance_id=0)
        if page_photos.exists():
            self.stdout.write('Deleting %s PagePhoto without instance' % page_photos.count())
            page_photos.delete()

        page_files = PageFile.objects.filter(instance_id=0)
        if page_files.exists():
            self.stdout.write('Deleting %s PageFiles without instance' % page_files.count())
            page_files.delete()

        simple_photos = SimplePhoto.objects.filter(instance_id=0)
        if simple_photos.exists():
            self.stdout.write('Deleting %s SimplePhoto without instance' % simple_photos.count())
            simple_photos.delete()

        for app in self.get_apps():
            for model in apps.get_models(app):
                if not model._meta.managed:
                    continue

                self.process_model(app, model)

        self.stdout.write('Done')
