import json
from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def js_storage_out(context):
    request = context.get('request')
    if not request:
        return ''

    output = ','.join(
        '"{0}": {1}'.format(key, json.dumps(val)) for key, val in request.js_storage.items()
    )
    return '<script type="text/javascript">var js_storage={{{0}}}</script>'.format(output)
