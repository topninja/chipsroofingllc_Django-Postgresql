from django.dispatch import receiver
from django.db.models.signals import post_delete
from ..models import PageFile


@receiver(post_delete)
def delete_file(sender, **kwargs):
    """
        Удаление файла при удалении сущности
    """
    instance = kwargs.get('instance')
    if isinstance(instance, PageFile):
        instance.file.delete(save=False)
