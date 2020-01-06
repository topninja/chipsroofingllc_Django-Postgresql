"""
    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.autocomplete',
                ...
            )

        urls.py:
            ...
            url(r'^autocomplete/', include('libs.autocomplete.urls', namespace='autocomplete')),
            ...

    Необязательные настройки:
        AUTOCOMPLETE_CACHE_BACKEND = 'default'

    Пример:
        # page/models.py:
            class SubType(models.Model):
                ...

                @staticmethod
                def autocomplete_item(obj):
                    # Свой формат пунктов списка
                    text = '–' * obj.level + obj.title
                    return {
                        'id': obj.pk,
                        'text': '<span style="color: red;">%s</span>' % text,
                        'selected_text': '<span style="color: green;">%s</span>' % text,
                    }

        # page/admin.py:
            class PostAdminForm(forms.ModelForm):

                class Meta:
                    widgets = {
                        'post_subtype': AutocompleteWidget(
                            filters = (
                                ('sections', 'sections', True),
                            ),
                            attrs = {
                                'style': 'width:50%',
                            },
                            min_chars = 2,
                            format_item = SubType.autocomplete_item,
                        )
                    }


    Также, включает фильтр для списка сущностей в админке:
        from django.utils.translation import get_language
        from libs.autocomplete import AutocompleteListFilter


        class PublicationTagFilter(AutocompleteListFilter):
            model = Tag
            multiple = False

            def filter(self, queryset, value):
                return queryset.filter(tags=value).distinct()


        class PublicationAdmin(admin.ModelAdmin):
            ...
            list_filter = (PublicationTagFilter, ...)

            @property
            def media(self):
                return super().media + forms.Media(
                    js=(
                        'autocomplete/js/select2.min.js',
                        'autocomplete/js/select2_cached.js',
                        'autocomplete/js/select2_locale_%s.js' % get_language(),
                        'autocomplete/js/filter.js',
                    ),
                    css={
                        'all': (
                            'autocomplete/css/select2.css',
                        )
                    }
                )
"""
