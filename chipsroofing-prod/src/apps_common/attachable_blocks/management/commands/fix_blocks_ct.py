from django.apps import apps
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType
from ...models import AttachableBlock, AttachableReference


class Command(BaseCommand):
    """
        Установка блокам и ссылкам на блоки правильных значений ContentType
    """
    help = 'Fix broken ContentType references'

    def handle(self, *args, **options):
        for model in apps.get_models():
            if issubclass(model, AttachableBlock) and model is not AttachableBlock:
                ct = ContentType.objects.get_for_model(model)

                # fix block ContentType
                model.objects.update(content_type=ct.pk)

                # fix reference ContentType
                AttachableReference.objects.filter(block__in=model.objects.values('pk')).update(block_ct=ct.pk)

        print('Done')
