"""
    Зависит от:
        libs.variation_field

    Настройки:
        STDIMAGE_MAX_SIZE_DEFAULT = 12*1024*1024
        STDIMAGE_MIN_DIMENSIONS_DEFAULT = (0, 0)
        STDIMAGE_MAX_DIMENSIONS_DEFAULT = (6000, 6000)
        STDIMAGE_MAX_SOURCE_DIMENSIONS_DEFAULT = (2048, 2048)

    Пример:
        preview = StdImageField(_('preview'),
            blank=True,
            storage=MediaStorage('main/header'),
            min_dimensions=(800, 600),
            admin_variation='admin',
            crop_area=True,
            aspects='normal',
            variations=dict(
                normal=dict(
                    size=(800, 600),
                ),
                admin=dict(
                    size=(200, 150),
                ),
            ),
        )

    Пример с сохранением области обрезки в отдельном поле:
        preview = StdImageField(_('preview'),
            blank=True,
            storage=MediaStorage('main/header'),
            admin_variation='admin',
            crop_area=True,
            crop_field='preview_crop',
            aspects=('normal', ),
            variations=dict(
                normal=dict(
                    size=(800, 600),
                ),
                admin=dict(
                    size=(200, 150),
                    mask='module/img/square_mask.png',
                    overlay='module/img/square_overlay.png',
                ),
            ),
        )
        preview_crop = models.CharField(_('stored_crop'),
            max_length=32,
            blank=True,
            editable=False,
        )

"""
