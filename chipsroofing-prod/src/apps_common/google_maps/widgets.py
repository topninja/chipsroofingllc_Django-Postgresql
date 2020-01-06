from django import forms
from . import conf


class GoogleCoordsAdminWidget(forms.TextInput):
    attrs = None

    class Media:
        css = {
            'all': (
                'google_maps/admin/css/google_maps.css',
            )
        }
        js = (
            'google_maps/js/core.js',
            'google_maps/admin/js/google_maps.js',
        )

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}

        attrs['data-width'] = attrs.pop('width', conf.ADMIN_MAP_WIDTH)
        attrs['data-height'] = attrs.pop('height', conf.ADMIN_MAP_HEIGHT)
        attrs['data-zoom'] = attrs.pop('zoom', conf.ADMIN_MAP_ZOOM)

        defaults = {
            'class': 'google-map-field',
        }
        defaults.update(attrs)

        super().__init__(defaults)
