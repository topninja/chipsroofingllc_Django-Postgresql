"""
    Поля для хранения цвета и цвета с прозрачностью.

    Пример:
        color = ColorField(_('color'), blank=True, default='#FF0000')
        color2 = ColorOpacityField(_('color'), blank=True, default='#FF0000:0.75')


        > instance.color
        '#FFFF00'

        > instance.color.rgb
        'rgb(255, 255, 0)'

        > instance.color.rgba
        'rgba(255, 255, 0, 1)'
"""
