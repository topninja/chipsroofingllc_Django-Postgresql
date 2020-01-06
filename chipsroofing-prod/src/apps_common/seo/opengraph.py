from django.utils.html import strip_tags
from django.template.defaultfilters import truncatechars
from django.db.models.fields.files import ImageFieldFile


class MetaTags:
    def __init__(self, request):
        self._dict = {}
        self.request = request

    def update(self, *args, **kwargs):
        self._dict.update(*args, **kwargs)
        self._format()

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value
        self._format()

    def _format(self):
        # stringify all
        for key, value in tuple(self._dict.items()):
            new_value = self._format_value(key, value)
            if new_value:
                self._dict[key] = new_value
            else:
                del self._dict[key]

    def _format_value(self, key, value):
        if value:
            try:
                return strip_tags(str(value))
            except (TypeError, ValueError):
                pass

    def _format_image(self, image):
        if isinstance(image, ImageFieldFile):
            return self.request.build_absolute_uri(image.url)
        elif isinstance(image, str) and not image.startswith('http'):
            return self.request.build_absolute_uri(image)

    @property
    def data(self):
        return self._dict


class Opengraph(MetaTags):
    OG_PREFIXED = ('url', 'title', 'image', 'description', 'type')

    def __init__(self, request):
        super().__init__(request)
        self._dict['type'] = 'website'

    def _format(self):
        image = self._dict.get('image')
        if image:
            self._dict['image'] = self._format_image(image)

        super()._format()

    @property
    def data(self):
        final_data = {}
        for key, value in self._dict.items():
            if key in self.OG_PREFIXED:
                final_data['og:%s' % key] = value
            else:
                final_data[key] = value

        return final_data


class TwitterCard(MetaTags):
    ALLOWED = ('card', 'title', 'description', 'image')

    def __init__(self, request):
        super().__init__(request)
        self._dict['card'] = 'summary'

    def _format_value(self, key, value):
        if key not in self.ALLOWED:
            return
        return super()._format_value(key, value)

    def _format(self):
        image = self._dict.get('image')
        if image:
            self._dict['image'] = self._format_image(image)

            if isinstance(image, ImageFieldFile):
                image_size = image._get_image_dimensions()
                is_large = image_size[0] >= 500 and image_size[1] >= 250
                self._dict['card'] = 'summary_large_image' if is_large else 'summary'

        super()._format()

        # title
        title = self._dict.get('title')
        if title:
            self._dict['title'] = truncatechars(title, 70)

        # description
        descr = self._dict.get('description')
        if descr:
            self._dict['description'] = truncatechars(descr, 200)

