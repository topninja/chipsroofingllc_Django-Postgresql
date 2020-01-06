"""
    Зависит от:
        libs.aliased_queryset
        libs.form_helper
        libs.storages
        libs.upload
        libs.variation_field
        libs.videolink_field

    Настройки:
        GALLERY_MAX_SIZE_DEFAULT = 12*1024*1024
        GALLERY_MIN_DIMENSIONS_DEFAULT = (0, 0)
        GALLERY_MAX_DIMENSIONS_DEFAULT = (6000, 6000)
        GALLERY_MAX_SOURCE_DIMENSIONS_DEFAULT = (2048, 2048)
        GALLERY_ADMIN_CLIENT_RESIZE_DEFAULT = False

    Команды:
        pm check_galleries
        Проверка всех галерей на наличие привязки к сущности, пустоту и битые картинки

    Пример:
        models.py:
            from gallery.fields import GalleryField
            from gallery.models import GalleryImageItem, GalleryVideoLinkItem, GalleryBase

            class PostGalleryImageItem(GalleryImageItem):
                STORAGE_LOCATION = 'module/gallery'
                MIN_DIMENSIONS = (400, 300)
                ADMIN_CLIENT_RESIZE = True
                ADMIN_VARIATION = 'admin'
                SHOW_VARIATION = 'normal'
                ASPECTS = 'normal'
                VARIATIONS = dict(
                    normal=dict(
                        size=(400, 300)
                    ),
                    micro=dict(
                        size=(120, 100),
                    ),
                    admin=dict(
                        size=(160, 120),
                    ),
                )

            class PostGalleryVideoLinkItem(GalleryVideoLinkItem):
                STORAGE_LOCATION = 'module/gallery'
                ADMIN_VARIATION = 'admin'
                VARIATIONS = dict(
                    wide=dict(
                        size=(1024, 576),
                        stretch=True,
                    ),
                    normal=dict(
                        size=(640, 480),
                        stretch=True,
                    ),
                    mobile=dict(
                        size=(480, 360),
                    ),
                    admin=dict(
                        size=(160, 120),
                    ),
                )

            class PostGallery(GalleryBase):
                IMAGE_MODEL = PostGalleryImageItem
                VIDEO_LINK_MODEL = PostGalleryVideoLinkItem

            class MyModel(models.Model):
                ...
                gallery = GalleryField(PostGallery, verbose_name=_('gallery'), blank=True, null=True)

        template.html:
            {% if config.gallery and config.gallery.image_items %}
                ...
                    {% for item in config.gallery.image_items %}
                        <img class="{% if forloop.first %}first{% endif %}"
                             src="{{ item.image.normal.url }}"
                             alt=""
                             width="{{ item.image.normal.dimensions.0 }}"
                             height="{{ item.image.normal.dimensions.1 }}">
                    {% endfor %}
                ...
            {% endif %}

    Перенарезка всех картинок галереи:
        1) MyImageItem.recut_all('mobile')
            или
           MyGallery.IMAGE_MODEL.recut_all('mobile')

        2) for item in gallery.image_items:
               item.image.recut()

        3) for error_code, msg in gallery.recut_generator():
               print(msg)
               if error_code:
                   break

    Копирование элементов в другую галерею:
        source_gallery.copy_items_to(dest_gallery)
        source_gallery.copy_items_to(dest_gallery, items=(23, 45, 34))
        source_gallery.copy_items_to(dest_gallery, items=source_gallery.image_items)
"""
