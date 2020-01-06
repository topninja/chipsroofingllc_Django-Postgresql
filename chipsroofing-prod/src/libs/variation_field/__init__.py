"""
    Модуль, предоставляющий базовые методы и классы для
    работы с вариациями картинок.

    Пример:
        from libs.variation_field.utils import process_image

        img, params = process_image('source.jpeg', size=(1092, 0), crop=False, quality=90)
        img.save('dest.jpg', optimize=1, **params)

"""
