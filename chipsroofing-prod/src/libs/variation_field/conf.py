from django.conf import settings

# Форматы, допустимые для указания в вариации
ALLOWED_FORMATS = ('jpeg', 'jpg', 'png', 'gif')

# Форматы, допустимые в PIL
FORMAT_JPEG = 'JPEG'
FORMAT_PNG = 'PNG'
FORMAT_GIF = 'GIF'

# Карта определения расширения файлов
FORMAT_EXT = {
    FORMAT_JPEG: 'jpg',
    FORMAT_PNG: 'png',
    FORMAT_GIF: 'gif',
}


DEFAULT_VARIATION = dict(
    # Размер
    size=(),

    stretch=False,
    crop=True,

    # Максимальные размеры результата.
    # Используется только при crop=False
    max_width=0,
    max_height=0,

    # Влияет на то, какие части картинки обрезаются при crop=True.
    # Также определяет положение картинки по отношению к холсту.
    center=(0.5, 0.5),

    # Цвет фона, на который накладывается изображение, когда оно не может сохранить прозрачность
    background=(255, 255, 255, 0),

    # Файл-маска для обрезания картинки
    mask=None,

    # Файл, накладываемый на картинку
    overlay=None,

    # Настройки наложения водяного знака.
    # Например:
    #   watermark = {
    #       file: 'img/watermark.png',
    #       position: 'C',
    #       padding: (20, 30),
    #       opacity: 1,
    #       scale: 1,
    #   }
    watermark=None,

    # Требуемый формат изображения (JPEG/PNG/GIF)
    format=None,

    # Сохранить EXIF
    exif=False,

    # Качество результата картинки (0-100)
    quality=None,
)


DEFAULT_WATERMARK = {
    'file': '',
    'position': 'C',
    'padding': (0, 0),
    'opacity': 1,
    'scale': 1,
}

# Количество потоко при нарезке вариаций
VARIATION_THREADS = getattr(settings, 'VARIATION_THREADS', 1)
