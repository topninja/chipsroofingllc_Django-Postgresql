"""
    Модуль, позволяющий создавать HTML-блоки определенных типов,
    привязывать их к конкретным страницам и менять порядок их следования
    через интерфейс администратора.

    Зависит от:
        libs.autocomplete

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'attachable_blocks',
                ...
            )

        urls.py:
            ...
            url(r'^blocks/', include('attachable_blocks.urls', namespace='blocks')),
            ...


    1. Для каждого блока должна быть создана модель, зарегистрированная в админке.
    2. Для каждого блока должна быть создана функция рендеринга.
    3. Для массового вывода блоков нужно добавить inline в админскую модель страницы,
       к которой нужно присоединять блоки.
    4. В тех случаях, когда к одной модели необходимо подключить несколько наборов блоков
       (например, когда последовательность выводимых блоков не является непрерывной),
       каждая inline-модель блоков админки должна иметь уникальное для модели-приемника значение
       текстового атрибута set_name. Значение set_name по умолчанию равно 'default'.

    Пример создания блока:
        # blocks/models.py:
            from attachable_blocks.models import AttachableBlock

            class MyBlock(AttachableBlock):
                BLOCK_VIEW = 'blocks.views.my_block_render'

                title = models.CharField(_('title'), max_length=255, blank=True)

                class Meta:
                    verbose_name = _('My block')
                    verbose_name_plural = _('My blocks')

        # blocks/admin.py
            from attachable_blocks.admin import AttachableBlockAdmin
            from .models import MyBlock

            @admin.register(MyBlock)
            class MyBlockAdmin(AttachableBlockAdmin):
                fieldsets = AttachableBlockAdmin.fieldsets + (
                    (_('Private'), {
                        'classes': ('suit-tab', 'suit-tab-general'),
                        'fields': ('title', ),
                    }),
                )


        # blocks/views.py:
            def my_block_render(context, block, **kwargs):
                return loader.render_to_string('block.html', {
                    'block': block,
                }, request=context.get('request'))


    Пример вывода конкретного блока любого типа на странице (никакой привязки к странице не требуется):
        # page/views.py:
            from blocks.models import MyBlock

            def index(request, ...):
                ...
                block = MyBlock.objects.filter(visible=True).first()
                context = RequestContext(request, {
                    ...
                    'block': block,
                })
                ...

        # page/template.html:
            {% load attached_blocks %}

            <!-- вывод конкретного блока -->
            {% render_attachable_block block ajax=True %}

            <!-- вывод первого попавшегося блока заданной модели -->
            {% render_attachable_block 'module.BlockModel' ajax=True %}

    Пример связи блоков с конкретной страницей через модель:
        # page/models.py:
            from attachable_blocks.fields import AttachableBlockField
            from blocks.models import MyBlock

            class MyPage(models.Model):
                ...
                my_block = AttachableBlockField(MyBlock, verbose_name=_('block instance'))

        # page/template.html:
            {% load attached_blocks %}

            <!-- вывод блока, привязанного к модели -->
            {% render_attachable_block page.my_block %}


    Пример массового подключения блоков к странице:
        # page/admin.py:
            from attachable_blocks.admin import AttachedBlocksTabularInline

            class FirstBlocksInline(AttachedBlocksTabularInline):
                # Первый набор блоков (set_name = 'default')
                verbose_name = 'My first block'
                verbose_name_plural = 'My first blocks'
                suit_classes = 'suit-tab suit-tab-blocks'

            class SecondBlocksInline(AttachedBlocksTabularInline):
                # Второй набор блоков
                set_name = 'second'
                verbose_name = 'My second block'
                verbose_name_plural = 'My second blocks'
                suit_classes = 'suit-tab suit-tab-blocks'

            class MyPageAdmin(admin.ModelAdmin):
                ...
                inlines = (FirstBlocksInline, SecondBlocksInline, ...)
                ...
                suit_form_tabs = (
                    ...
                    ('blocks', _('Blocks')),
                    ...
                )

        # template.html:
            {% load attached_blocks %}

            <!-- вывод блоков первого набора (set_name = 'default') -->
            {% render_attached_blocks page_object %}

            <!-- вывод блоков второго набора (set_name = 'second') -->
            {% render_attached_blocks page_object set_name='second' %}

"""

default_app_config = 'attachable_blocks.apps.Config'
