from importlib import import_module
from django.db import models
from django.contrib.contenttypes.models import ContentType

# ContentType ID -> Model class
BLOCK_TYPES = {}

# Model class -> render function
BLOCK_VIEWS = {}


def get_model_by_ct(ct_id):
    """
        Возвращает модель блока по его ContentType ID
    """
    if ct_id in BLOCK_TYPES:
        return BLOCK_TYPES[ct_id]
    else:
        ct = ContentType.objects.get(pk=ct_id)
        BLOCK_TYPES[ct_id] = ct.model_class()
        return BLOCK_TYPES[ct_id]


def get_block_view(block):
    """
        Получение функции рендеринга блока
    """
    block_model = block._meta.concrete_model
    _cached = BLOCK_VIEWS.get(block_model, None)
    if _cached is not None:
        return _cached

    path = getattr(block_model, 'BLOCK_VIEW', '')
    if not path:
        return

    if '.' not in path:
        return

    module_path, view_name = path.rsplit('.', 1)
    try:
        module = import_module(module_path)
    except ImportError:
        return

    view = getattr(module, view_name, None)
    if view is None:
        return

    BLOCK_VIEWS[block_model] = view
    return view


def get_last_updated(instance):
    """
        Получение даты последнего изменения подключаемого блока,
        привязанного к сущности
    """
    from .models import AttachableBlock, AttachableReference
    attached_blocks = AttachableReference.get_for(instance).values_list('block', flat=True)
    result = AttachableBlock.objects.filter(pk__in=attached_blocks).aggregate(models.Max('updated'))
    return result['updated__max']
