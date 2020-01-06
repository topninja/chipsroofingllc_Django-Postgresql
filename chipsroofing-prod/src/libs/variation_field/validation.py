from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from .croparea import CropArea


def validate_type(value, error_messages=None):
    """ Валидация типа файла """
    error_messages = error_messages or {}

    try:
        Image.open(value).verify()
    except Exception:
        raise ValidationError(
            error_messages.get(
                'not_image',
                _("Image invalid or corrupted")
            ),
            code='not_image',
        )


def validate_dimensions(value, min_dimensions=(0, 0), max_dimensions=(0, 0), croparea=None, error_messages=None):
    """ Валидация размеров картинки """
    error_messages = error_messages or {}

    img_width, img_height = Image.open(value).size
    if croparea:
        croparea = CropArea(croparea)
        img_width = min(croparea.width, img_width)
        img_height = min(croparea.height, img_height)

    min_width, min_height = min_dimensions
    if min_width and img_width < min_width:
        raise ValidationError(
            error_messages.get(
                'not_enough_width',
                _('Image should not be less than %(limit)spx in width')
            ) % {
                'current': img_width,
                'limit': min_width,
            },
            code='not_enough_width',
        )
    if min_height and img_height < min_height:
        raise ValidationError(
            error_messages.get(
                'not_enough_height',
                _('Image should not be less than %(limit)spx in height')
            ) % {
                'current': img_height,
                'limit': min_height,
            },
            code='not_enough_height',
        )

    max_width, max_height = max_dimensions
    if max_width and img_width > max_width:
        raise ValidationError(
            error_messages.get(
                'too_much_width',
                _('Image should not be more than %(limit)spx in width')
            ) % {
                'current': img_width,
                'limit': max_width,
            },
            code='too_much_width',
        )
    if max_height and img_height > max_height:
        raise ValidationError(
            error_messages.get(
                'too_much_height',
                _('Image should not be more than %(limit)spx in height')
            ) % {
                'current': img_height,
                'limit': max_height,
            },
            code='too_much_height',
        )


def validate_size(value, max_size=20*1024*1024, error_messages=None):
    """ Валидация веса картинки """
    error_messages = error_messages or {}

    if max_size and value.size > max_size:
        raise ValidationError(
            error_messages.get(
                'too_big',
                _('Image must be no larger than %(limit)s')
            ) % {
                'current': filesizeformat(value.size),
                'limit': filesizeformat(max_size),
            },
            code='too_big',
        )
