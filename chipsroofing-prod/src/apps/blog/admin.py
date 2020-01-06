from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from social_networks.admin import AutoPostMixin
from attachable_blocks.admin import AttachedBlocksStackedInline, AttachableBlockAdmin
from libs.autocomplete.widgets import AutocompleteMultipleWidget
from .models import BlogConfig, BlogPost, Tag, BlogBlock


class BlogConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(BlogConfig)
class BlogConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('background', 'background_alt', 'title', 'description', 'text'),
        }),
    )
    inlines = (BlogConfigBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )


@admin.register(Tag)
class TagAdmin(ModelAdminMixin, SortableModelAdmin):
    """ Тэг """
    fieldsets = (
        (None, {
            'fields': ('title', 'slug'),
        }),
    )
    sortable = 'sort_order'
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'tags': AutocompleteMultipleWidget(),
        }


@admin.register(BlogPost)
class BlogPostAdmin(SeoModelAdminMixin, AutoPostMixin, admin.ModelAdmin):
    """ Пост """
    fieldsets = (
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (('background', 'preview'), 'background_alt', 'alt', 'header', 'slug', 'tags', 'status', 'date'),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('note', 'text'),
        }),
    )
    form = BlogPostForm
    list_filter = ('status',)
    date_hierarchy = 'date'
    search_fields = ('header',)
    list_display = ('view', '__str__', 'tags_list', 'date_fmt', 'status')
    list_display_links = ('__str__',)
    actions = ('make_public_action', 'make_draft_action')
    prepopulated_fields = {
        'slug': ('header',)
    }

    suit_form_tabs = (
        ('general', _('General')),
    )

    def tags_list(self, obj):
        return ' / '.join((str(item.title) for item in obj.tags.all()))

    tags_list.short_description = _('tags')

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)

    date_fmt.short_description = _('Publication date')
    date_fmt.admin_order_field = 'date'

    def get_autopost_text(self, obj):
        return obj.note

    def make_public_action(self, request, queryset):
        queryset.update(status=self.model.STATUS_PUBLIC)

    make_public_action.short_description = _('Make public')

    def make_draft_action(self, request, queryset):
        queryset.update(status=self.model.STATUS_DRAFT)

    make_draft_action.short_description = _('Make draft')


@admin.register(BlogBlock)
class BlogBlockAdmin(AttachableBlockAdmin):
    """ Подключаемый блок блога """
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Customization'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
