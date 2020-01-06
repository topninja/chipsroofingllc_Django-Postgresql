from django.apps import apps
from django.template import Library
from django.forms.utils import flatatt
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableBlock, AttachableReference
from ..utils import get_model_by_ct, get_block_view

register = Library()


def block_output(context, block, ajax=False, **kwargs):
    """
        Возвращает отрендеренный HTML блока или заглушку для AJAX-запроса
    """
    block_view = get_block_view(block)
    if not block_view:
        return ''

    if ajax:
        # Блок, загружаемый через AJAX
        attrs = {
            'data-id': block.id,
        }
        instance = kwargs.get('instance')
        if instance is None:
            attrs['data-cid'] = ''
            attrs['data-oid'] = ''
        else:
            attrs['data-cid'] = ContentType.objects.get_for_model(instance).pk
            attrs['data-oid'] = instance.pk

        block_html = '<div class="async-block" {attrs}></div>'.format(
            attrs=flatatt(attrs)
        )
    else:
        block_html = block_view(context, block, **kwargs)

    return block_html


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, instance, set_name='default', **kwargs):
    output = []
    kwargs.setdefault('instance', instance)

    references = AttachableReference.get_for(instance, set_name=set_name)
    for reference in references.only('block_ct', 'block_id', 'ajax'):
        block_model = get_model_by_ct(reference.block_ct_id)
        block = block_model.objects.get(pk=reference.block_id)

        block_html = block_output(context, block, ajax=reference.ajax, **kwargs)
        if block_html:
            output.append(block_html)

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block, ajax=False, instance=None, **kwargs):
    if block is None:
        return ''

    if issubclass(block._meta.concrete_model, AttachableBlock):
        block_model = get_model_by_ct(block.content_type_id)
        block = block_model.objects.get(pk=block.pk)

    if block.visible:
        return block_output(context, block, ajax=ajax, instance=instance, **kwargs)
    else:
        return ''


@register.simple_tag(takes_context=True)
def render_first_attachable_block(context, model_path, ajax=False, instance=None, **kwargs):
    if '.' not in model_path:
        return ''

    app, modelname = model_path.rsplit('.', 1)
    try:
        model = apps.get_model(app, modelname)
    except LookupError:
        return ''

    block = model.objects.first()
    if not block:
        return ''

    return render_attachable_block(context, block, ajax=ajax, instance=instance, **kwargs)
