from django.template import Library, loader

register = Library()


def estimate_block_render(context, block, **kwargs):
    return loader.render_to_string('blocks/estimate.html', {
        'is_main_page': context.get('is_main_page'),
        'block': block,
    }, request=context.get('request'))


def partners_block_render(context, block, **kwargs):
    return loader.render_to_string('blocks/partners.html', {
        'block': block,
    }, request=context.get('request'))

def videos_render(context, block, **kwargs):
    return loader.render_to_string('blocks/videos.html', {
        'block': block,
    }, request=context.get('request'))
