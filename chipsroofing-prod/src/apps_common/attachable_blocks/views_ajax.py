from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseForbidden, JsonResponse
from .models import AttachableBlock
from .utils import get_model_by_ct, get_block_view


@csrf_exempt
def get_blocks(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    block_ids = request.GET.get('block_ids')
    if not block_ids:
        return JsonResponse({})

    try:
        cid = int(request.GET.get('cid'))
        oid = int(request.GET.get('oid'))
    except (TypeError, ValueError):
        instance = None
    else:
        try:
            ct = ContentType.objects.get(pk=cid)
        except ContentType.DoesNotExist:
            return JsonResponse({})

        ct_model = ct.model_class()
        try:
            instance = ct_model.objects.get(pk=oid)
        except ct_model.DoesNotExists:
            return JsonResponse({})

    result = {}
    for block_id in block_ids.split(','):
        try:
            block_id = int(block_id)
        except (TypeError, ValueError):
            continue

        block_ct_id = AttachableBlock.objects.filter(pk=block_id).values_list('content_type', flat=True).first()
        block_model = get_model_by_ct(block_ct_id)
        block = block_model.objects.get(pk=block_id)

        if not block.visible:
            continue

        block_view = get_block_view(block)
        if not block_view:
            continue

        result[block_id] = block_view(RequestContext(request, {
            'request': request,
        }), block, instance=instance)

    return JsonResponse(result)
