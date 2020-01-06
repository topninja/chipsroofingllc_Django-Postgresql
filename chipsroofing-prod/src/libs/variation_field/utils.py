import operator
import itertools
from PIL import Image, ImageOps, ImageEnhance
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from .croparea import CropArea
from .size import Size
from . import conf


def is_size(value):
    """ Проверка, что value - это кортеж из двух неотрицательных чисел """
    if not isinstance(value, tuple):
        return False
    elif len(value) != 2:
        return False

    try:
        return all(int(item) >= 0 for item in value)
    except (TypeError, ValueError):
        return False


def limited_size(size, limit_size):
    """
        Пропорциональное уменьшение размера size, чтобы он не превосходил limit_size.
        Допустимо частичное указание limit_size, например, (1024, 0).
        Если size умещается в limit_size, возвращает None
    """
    max_width, max_height = limit_size
    if not max_width and not max_height:
        return None

    width, height = size
    if max_width and width > max_width:
        height = height * (max_width / width)
        width = max_width
    if max_height and height > max_height:
        width = width * (max_height / height)
        height = max_height
    width, height = round(width), round(height)
    if size == (width, height):
        return None

    return width, height


def split_every(n, iterable):
    i = iter(iterable)
    piece = list(itertools.islice(i, n))
    while piece:
        yield piece
        piece = list(itertools.islice(i, n))


def image_hash(image, hash_size=12):
    """
        Рассчет хэша картинки
    """
    if hash_size ** 2 % 8:
        raise ValueError('"size**2" must be divisible by 8')

    image.seek(0)

    # Grayscale and shrink
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS
    )

    # Compare adjacent pixels
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    hex_string = []
    for bin_array in split_every(8, difference):
        hex_string.append(
            '{0:02x}'.format(int(''.join(str(int(_)) for _ in bin_array), 2))
        )

    return ''.join(hex_string)


def check_variations(variations, obj):
    from django.core import checks
    errors = []

    for name, params in variations.items():
        if isinstance(params, tuple):
            params = {
                'size': params,
            }

        params = dict(conf.DEFAULT_VARIATION, **params)

        if not isinstance(params, dict):
            errors.append(checks.Error('variation %r should be a dict or tuple' % name, obj=obj))

        if not params:
            errors.append(checks.Error('variation %r is empty' % name, obj=obj))

        # size
        if 'size' not in params:
            errors.append(checks.Error('variation %r requires \'size\' value' % name, obj=obj))
        if not is_size(params['size']):
            errors.append(checks.Error(
                '"size" in variation %r should be a tuple of 2 non-negative numbers' % name, obj=obj
            ))

        # crop
        if not isinstance(params['crop'], bool):
            errors.append(checks.Error('"crop" in variation %r must be a boolean' % name, obj=obj))

        # stretch
        if not isinstance(params['stretch'], bool):
            errors.append(checks.Error('"stretch" in variation %r must be a boolean' % name, obj=obj))

        # max_width and max_height
        if not isinstance(params['max_width'], int) or params['max_width'] < 0:
            errors.append(checks.Error('"max_width" in variation %r must be a non-negative integer' % name, obj=obj))
        if not isinstance(params['max_height'], int) or params['max_height'] < 0:
            errors.append(checks.Error('"max_height" in variation %r must be a non-negative integer' % name, obj=obj))
        if params['crop'] and (params['max_width'] or params['max_height']):
            errors.append(checks.Error(
                '"max_width" and "max_height" allowed only when crop=False in variation %r' % name, obj=obj
            ))

        if not any(d for d in params['size']) and not params['max_width'] and not params['max_height']:
            errors.append(checks.Error('"size" in variation %r is empty and non-calulatable' % name, obj=obj))

        # center
        if 'center' in params:
            if params['center'] and not isinstance(params['center'], (list, tuple)):
                errors.append(checks.Error('"center" in variation %r should be a tuple or list' % name, obj=obj))

        # format
        if params['format']:
            fmt = str(params['format']).upper()
            if fmt not in conf.ALLOWED_FORMATS:
                errors.append(checks.Error(
                    'unacceptable format of variation %r: %r. Allowed types: %s' % (
                        name,
                        fmt,
                        ', '.join(conf.ALLOWED_FORMATS)
                    ),
                    obj=obj
                ))

        # overlay
        if params['overlay'] and not find(params['overlay']):
            errors.append(checks.Error('overlay file not found: %r' % params['overlay'], obj=obj))

        # mask
        if params['mask'] and not find(params['mask']):
            errors.append(checks.Error('mask file not found: %r' % params['mask'], obj=obj))

        if params['watermark']:
            watermark = dict(conf.DEFAULT_WATERMARK, **params['watermark'])

            if not isinstance(watermark, dict):
                errors.append(checks.Error('watermark settings should be a dict', obj=obj))

            # file
            if 'file' not in watermark:
                errors.append(checks.Error('watermark file required for variation %r' % name, obj=obj))
            if not find(watermark['file']):
                errors.append(checks.Error('watermark file not found: %r' % watermark['file'], obj=obj))

            # padding
            if not isinstance(watermark['padding'], (list, tuple)):
                errors.append(checks.Error('watermark\'s padding should be a tuple or list', obj=obj))
            try:
                watermark['padding'] = tuple(map(int, watermark['padding']))
            except (ValueError, TypeError):
                errors.append(checks.Error('invalid watermark padding: %r' % watermark['padding'], obj=obj))

            # opacity
            try:
                watermark['opacity'] = float(watermark['opacity'])
            except (TypeError, ValueError):
                errors.append(checks.Error('watermark\'s opacity should be a float', obj=obj))
            else:
                if watermark['opacity'] < 0 or watermark['opacity'] > 1:
                    errors.append(checks.Error('watermark\'s opacity should be in interval [0, 1]', obj=obj))

            # scale
            try:
                watermark['scale'] = float(watermark['scale'])
            except (TypeError, ValueError):
                errors.append(checks.Error('watermark\'s scale should be a float', obj=obj))
            else:
                if watermark['scale'] <= 0:
                    errors.append(checks.Error('watermark\'s scale should be greater than 0', obj=obj))

            # position
            watermark['position'] = str(watermark['position']).upper()
            if watermark['position'] not in ('TL', 'TR', 'BL', 'BR', 'C'):
                errors.append(checks.Error('watermark\'s position should be in (TL, TR, BL, BR, C)', obj=obj))

    return errors


def format_variation(**params):
    """
        Приведение настроек вариации к каноническому виду
    """
    variation = dict(conf.DEFAULT_VARIATION, **params)

    # Проверка формата
    image_format = variation.get('format')
    if image_format:
        image_format = str(image_format).upper()
        if image_format in ('JPEG', 'JPG'):
            image_format = conf.FORMAT_JPEG
    elif variation.get('mask'):
        # Не указан формат, но указана маска - переводим в PNG
        image_format = conf.FORMAT_PNG
    variation['format'] = image_format

    # Overlay
    overlay = variation.get('overlay')
    if overlay:
        variation['overlay'] = staticfiles_storage.path(overlay)

    # Mask
    mask = variation.get('mask')
    if mask:
        variation['mask'] = staticfiles_storage.path(mask)

    # Водяной знак
    watermark = variation.get('watermark')
    if watermark and isinstance(watermark, dict):
        watermark = dict(conf.DEFAULT_WATERMARK, **watermark)
        watermark['file'] = staticfiles_storage.path(watermark['file'])
        watermark['padding'] = tuple(map(int, watermark['padding']))
        watermark['opacity'] = float(watermark['opacity'])
        watermark['scale'] = float(watermark['scale'])
        watermark['position'] = str(watermark['position']).upper()
        variation['watermark'] = watermark

    return variation


def format_variations(variations):
    """ Форматирование вариаций """
    return {
        name: dict(format_variation(**params), name=name)
        for name, params in variations.items()
    }


def format_aspects(value, variations):
    """ Форматирование аспектов """
    result = []
    aspects = value if isinstance(value, tuple) else (value,)
    for aspect in aspects:
        try:
            aspect = float(aspect)
        except (TypeError, ValueError):
            if aspect not in variations:
                continue

            size = variations[aspect]['size']
            if all(d > 0 for d in size):
                aspect = operator.truediv(*size)
            else:
                continue

        result.append(str(round(aspect, 4)))
    return tuple(result)


def calculate_sizes(image, variation):
    """
        Рассчитывает финальные размеры изображения и холста.
    """
    crop = bool(variation['crop'])
    stretch = bool(variation['stretch'])

    source_size = image.size
    target_size = list(variation['size'])

    if crop:
        # Если указан только одна сторона - вторую берем из исходника
        if not target_size[0]:
            target_size[0] = source_size[0]
        elif not target_size[1]:
            target_size[1] = source_size[1]

        if not stretch:
            # если в вариации указана большая длина, чем у исходника - оставляем длину исходника
            target_size = (
                min(source_size[0], target_size[0]),
                min(source_size[1], target_size[1])
            )
        return target_size, target_size
    else:
        # Размеры картинки, вписываемой в холст
        image_size = Size(*source_size)

        max_width = variation['max_width']
        max_height = variation['max_height']

        # корректируем ограничения
        max_width = min(max_width or target_size[0], target_size[0] or max_width)       # type: int
        max_height = min(max_height or target_size[1], target_size[1] or max_height)    # type: int

        # Определяем размеры картинки
        if stretch:
            if max_width:
                if max_height:
                    max_aspect = max_width / max_height
                    if image_size.aspect > max_aspect:
                        # картинка шире холста
                        image_size.width = max_width
                    else:
                        # картинка выше холста
                        image_size.height = max_height
                else:
                    # плавающая выcота
                    image_size.width = max_width
            else:
                if max_height:
                    # плавающая ширина
                    image_size.height = max_height
        else:
            # растягивать запрещено
            if max_width:
                image_size.max_width(max_width)
            if max_height:
                image_size.max_height(max_height)

        # Определение размера холста
        if target_size[0] == 0:
            target_size[0] = image_size.width
        if target_size[1] == 0:
            target_size[1] = image_size.height

        return (image_size.width, image_size.height), tuple(target_size)


def get_transparency_mask(image, info=None):
    """
        Возвращает маску прозрачности изображения или None
    """
    if image.mode in ('RGBA', 'LA'):
        return image.split()[-1]
    elif image.mode == 'L':
        return None
    else:
        # GIF, PNG8, PNG24
        info = info or image.info or {}
        transparency = info.get('transparency')
        if transparency is None:
            return

        mask = Image.new('L', image.size)
        if isinstance(transparency, bytes):
            trans_len = len(transparency)
            mask.putdata([
                transparency[index] if index < trans_len else 255
                for index in image.getdata()
                ])
        else:
            mask.putdata([
                0 if index == transparency else 255
                for index in image.getdata()
            ])
        return mask


def variation_crop(image, croparea=None):
    """ Обрезка по координатам """
    if not croparea:
        return image

    if not isinstance(croparea, CropArea):
        croparea = CropArea(croparea)

    if croparea.x2 > image.size[0]:
        croparea.width = image.size[0] - croparea.x

    if croparea.y2 > image.size[1]:
        croparea.height = image.size[1] - croparea.y

    cropped = image.crop((
        croparea.x,
        croparea.y,
        croparea.x2,
        croparea.y2
    ))
    cropped.format = image.format
    return cropped


def variation_resize(image, image_size, variation):
    """
        Изменение размера картинки в соответствии с вариацией
    """
    source_format = image.format
    source_size = image.size

    # Режим обработки
    crop = bool(variation['crop'])
    stretch = bool(variation['stretch'])
    if crop:
        # размер не меняется - оставляем как есть
        if image_size == source_size:
            return image

        image = ImageOps.fit(
            image,
            image_size,
            method=Image.ANTIALIAS,
            centering=variation['center']
        )
    else:
        if stretch:
            image = image.resize(image_size, resample=Image.ANTIALIAS)
        else:
            image.thumbnail(image_size, resample=Image.ANTIALIAS)

    image.format = source_format
    return image


def variation_watermark(image, **wm_settings):
    """ Наложение водяного знака на картинку """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    with open(wm_settings['file'], 'rb') as fp:
        watermark = Image.open(fp)
        info = watermark.info
        if watermark.mode not in ('RGBA', 'LA') and not (watermark.mode == 'P' and 'transparency' in info):
            watermark.putalpha(255)

        img_width, img_height = image.size
        wm_width, wm_height = watermark.size

        scale = wm_settings['scale']
        if scale != 1:
            watermark = watermark.resize((int(wm_width * scale), int(wm_height * scale)), Image.ANTIALIAS)
            wm_width, wm_height = watermark.size

        position = wm_settings['position']
        padding = wm_settings['padding']
        if position == 'TL':
            left = padding[0]
            top = padding[1]
        elif position == 'TR':
            left = img_width - wm_width - padding[0]
            top = padding[1]
        elif position == 'BL':
            left = padding[0]
            top = img_height - wm_height - padding[1]
        elif position == 'BR':
            left = img_width - wm_width - padding[0]
            top = img_height - wm_height - padding[1]
        elif position == 'C':
            top = (img_height - wm_height) // 2
            left = (img_width - wm_width) // 2
        else:
            left = top = padding

        opacity = wm_settings['opacity']
        if opacity < 1:
            alpha = watermark.convert('RGBA').split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        image.paste(watermark, (left, top), watermark)

    return image


def variation_overlay(image, overlay):
    """ Наложение оверлея на картинку """
    overlay_img = Image.open(overlay)

    if overlay_img.size != image.size:
        overlay_img = ImageOps.fit(overlay_img, image.size, method=Image.ANTIALIAS)

    transparency_mask = get_transparency_mask(overlay_img, overlay_img.info)
    image.paste(overlay_img, mask=transparency_mask)

    return image


def variation_mask(image, mask):
    """ Обрезка картинки по маске """
    mask_img = Image.open(mask).convert('L')

    if mask_img.size != image.size:
        mask_img = ImageOps.fit(mask_img, image.size, method=Image.ANTIALIAS)

    transparency_mask = get_transparency_mask(mask_img, mask_img.info)
    background = Image.new('RGBA', image.size)
    background.paste(image, mask=transparency_mask)

    return background


def process_variation(source, variation, quality=None, croparea=None):
    """ Обработка картинки в соответствии с вариацией """
    with open(source, 'rb') as fp:
        image = Image.open(fp)
        image.load()

    source_format = image.format
    source_info = image.info
    source_mode = image.mode

    dest_format = variation['format'] or source_format
    dest_info = dict(format=dest_format)
    dest_mode = source_mode

    background = variation['background']

    # Для JPEG и PNG
    if dest_format in (conf.FORMAT_JPEG, conf.FORMAT_PNG):
        # Включаем оптимизацию
        dest_info['optimize'] = True

        # Копируем EXIF
        if variation['exif']:
            for key in ('exif', 'icc_profile'):
                data = source_info.get(key)
                if not data:
                    continue
                dest_info[key] = data

    # Для JPEG
    if dest_format == conf.FORMAT_JPEG:
        # Включаем progressive
        dest_info['progressive'] = True

        # Качество
        quality = quality or variation.get('quality')
        if quality:
            dest_info['quality'] = int(quality)

    # ===================================

    # Обрезаем по рамке
    if croparea is not None:
        output = variation_crop(image, croparea)
    else:
        output = image

    # финальные размеры изображения и холста
    image_size, canvas_size = calculate_sizes(output, variation)

    # ресайз
    output = variation_resize(output, image_size, variation)
    transparency_mask = get_transparency_mask(output, source_info)

    # наложение на фон
    if image_size != canvas_size:
        center = variation['center']
        size_diff = list(itertools.starmap(operator.sub, zip(canvas_size, image_size)))
        image_offset = (int(size_diff[0] * center[0]), int(size_diff[1] * center[1]))
        if background[3] == 255:
            background = Image.new('RGB', canvas_size, background)
            background.paste(output, image_offset, mask=transparency_mask)
            dest_mode = 'RGB'
        else:
            background = Image.new('RGBA', canvas_size, background)
            background.paste(output, image_offset, mask=transparency_mask)
            dest_mode = 'RGBA'
        output = background
    elif transparency_mask is not None:
        if background[3] == 255:
            background = Image.new('RGB', canvas_size, background)
            background.paste(output, mask=transparency_mask)
            dest_mode = 'RGB'
        else:
            background = Image.new('RGBA', canvas_size, background)
            background.paste(output, mask=transparency_mask)
            dest_mode = 'RGBA'
        output = background

    # watermark
    watermark_options = variation['watermark']
    if watermark_options:
        output = variation_watermark(output, **watermark_options)

    # overlay
    overlay = variation['overlay']
    if overlay:
        # FIX: Дикие баги при добавлении оверлея к палитре
        if dest_mode == 'P':
            output = output.convert('RGBA')
            dest_mode = 'RGBA'
        output = variation_overlay(output, overlay)

    # mask
    mask = variation['mask']
    if mask:
        output = variation_mask(output, mask)
        dest_mode = 'RGBA'

    # ===================================

    if dest_format == conf.FORMAT_JPEG:
        if dest_mode in ('P', 'RGBA'):
            # FIX: нельзя сохранять mode P в JPEG
            output = output.convert('RGB')

    # Перенос прозрачного цвета
    if 'transparency' in source_info:
        transparency = source_info['transparency']
        if dest_format == conf.FORMAT_GIF:
            if isinstance(transparency, int):
                dest_info['transparency'] = transparency
        elif dest_format == conf.FORMAT_PNG:
            if dest_mode == 'RGB' and isinstance(transparency, (tuple, list)):
                dest_info['transparency'] = transparency
            elif dest_mode == 'P' and isinstance(transparency, (int, bytes)):
                dest_info['transparency'] = transparency

    return output, dest_info


def process_image(source, croparea=None, **params):
    """ Алиас для тестов. Обработка картинки в соответствии с вариацией """
    variation = format_variation(**params)
    return process_variation(source, variation, croparea=croparea)
