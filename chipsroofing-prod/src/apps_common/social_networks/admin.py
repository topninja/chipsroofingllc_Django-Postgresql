import re
import uuid
from html import unescape
from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.http.response import Http404, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from .models import SocialConfig, SocialLinks, FeedPost
from .forms import FeedPostForm, AutpostForm
from .widgets import TokenButtonWidget
from . import conf

re_newlines = re.compile(r'\n[\s\n]+')
AUTOPOST_FORM_PREFIX = 'autopost'
SPRITE_ICONS = (
    conf.NETWORK_TWITTER,
    conf.NETWORK_FACEBOOK,
    conf.NETWORK_GOOGLE,
    conf.NETWORK_LINKEDIN,
    'pinterest',
    'instagram',
)


class SocialConfigForm(forms.ModelForm):
    twitter_token = forms.CharField(
        label='',
        required=False,
        widget=TokenButtonWidget('Update access token'),
    )

    facebook_token = forms.CharField(
        label='',
        required=False,
        widget=TokenButtonWidget('Update access token'),
    )

    instagram_token = forms.CharField(
        label='',
        required=False,
        widget=TokenButtonWidget('Update access token'),
    )

    linkedin_token = forms.CharField(
        label='',
        required=False,
        widget=TokenButtonWidget('Update access token'),
    )

    class Meta:
        model = SocialConfig
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = SocialConfig.get_solo()

        # Twitter
        if config.twitter_client_id and config.twitter_client_secret and config.twitter_access_token_secret:
            from requests_oauthlib import OAuth1Session
            redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:twitter_token'))

            oauth_client = OAuth1Session(
                client_key=config.twitter_client_id,
                client_secret=config.twitter_client_secret,
                callback_uri=redirect_uri,
            )

            try:
                oauth_client.fetch_request_token('https://api.twitter.com/oauth/request_token')
            except ValueError:
                raise Http404

            token_url = oauth_client.authorization_url('https://api.twitter.com/oauth/authorize')

            self.fields['twitter_token'].initial = token_url
            self.fields['twitter_token'].help_text = _(
                'Add redirect URI "%s" to your Twitter application') % redirect_uri

        # Facebook
        if config.facebook_client_id and config.facebook_client_secret:
            redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:facebook_token'))
            token_url = ('https://www.facebook.com/dialog/oauth'
                         '?client_id={client_id}&redirect_uri={redirect_uri}'
                         '&scope={scope}&state=&response_type=code').format(
                client_id=config.facebook_client_id,
                redirect_uri=redirect_uri,
                scope='manage_pages,publish_pages',
            )
            self.fields['facebook_token'].initial = token_url
            self.fields['facebook_token'].help_text = _('Add redirect URI "%s" to your Facebook application') % redirect_uri

        # Instagram
        if config.instagram_client_id and config.instagram_client_secret:
            redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:instagram_token'))
            token_url = ('https://api.instagram.com/oauth/authorize/'
                         '?client_id={client_id}&redirect_uri={redirect_uri}'
                         '&response_type=code').format(
                client_id=config.instagram_client_id,
                redirect_uri=redirect_uri,
            )
            self.fields['instagram_token'].initial = token_url
            self.fields['instagram_token'].help_text = _('Add redirect URI "%s" to your Instagram application') % redirect_uri

        # LinkedIn
        if config.linkedin_client_id and config.linkedin_client_secret:
            redirect_uri = self.request.build_absolute_uri(resolve_url('admin_social_networks:linkedin_token'))
            token_url = ('https://www.linkedin.com/oauth/v2/authorization'
                         '?client_id={client_id}&redirect_uri={redirect_uri}'
                         '&response_type=code&state={state}&scope={scope}').format(
                client_id=config.linkedin_client_id,
                redirect_uri=redirect_uri,
                state=uuid.uuid1(),
                scope='r_basicprofile%20w_share',
            )
            self.fields['linkedin_token'].initial = token_url
            self.fields['linkedin_token'].help_text = _(
                'Add redirect URI "%s" to your LinkedIn application') % redirect_uri


@admin.register(SocialConfig)
class SocialConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (_('Google'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'google_apikey',
            ),
        }),
        (_('Twitter'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'twitter_client_id', 'twitter_client_secret', 'twitter_access_token', 'twitter_access_token_secret',
                'twitter_token',
            ),
        }),
        (_('Facebook'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'facebook_client_id', 'facebook_client_secret', 'facebook_access_token', 'facebook_token',
            ),
        }),
        (_('Instagram'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'instagram_client_id', 'instagram_client_secret', 'instagram_access_token', 'instagram_token',
            ),
        }),
        (_('LinkedIn'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'linkedin_client_id', 'linkedin_client_secret', 'linkedin_access_token', 'linkedin_token',
            ),
        }),
    )
    form = SocialConfigForm
    suit_form_tabs = (
        ('general', _('General')),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form.request = request
        return form


@admin.register(SocialLinks)
class SocialLinksAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'social_google', 'social_twitter', 'social_facebook', 'social_instagram',
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
    )


@admin.register(FeedPost)
class FeedPostAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'network', 'url', 'text', 'scheduled',
            ),
        }),
        (_('Information'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'created', 'posted'
            ),
        }),
    )
    form = FeedPostForm
    list_display = ('network_icon', '__str__', 'scheduled', 'created', 'posted')
    list_display_links = ('network_icon', '__str__')
    list_filter = ('network', 'created')
    readonly_fields = ('created', 'posted')
    actions = ('action_schedule_posts', 'action_unschedule_posts')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def suit_cell_attributes(self, obj, column):
        """ Классы для ячеек списка """
        default = super().suit_cell_attributes(obj, column)
        if column == 'network_icon':
            default.setdefault('class', '')
            default['class'] += ' mini-column'
        return default

    def network_icon(self, obj):
        icons_url = staticfiles_storage.url('social_networks/img/admin_icons.svg')
        try:
            icon_code, icon_title = next((
                network_tuple
                for network_tuple in conf.ALL_NETWORKS
                if network_tuple[0] == obj.network
            ))
        except StopIteration:
            return

        offset = 100 / (len(SPRITE_ICONS) - 1) * SPRITE_ICONS.index(icon_code)
        return """
        <span style="display:inline-block; width:21px; height:20px; margin:0;
        background:url(%s) %0.4f%% 0; vertical-align:middle;" title="%s"/>""" % (
            icons_url, offset, icon_title
        )

    network_icon.short_description = _('#')
    network_icon.allow_tags = True

    def action_schedule_posts(self, request, queryset):
        queryset.update(scheduled=True)

    action_schedule_posts.short_description = _('Schedule %(verbose_name_plural)s to publish')

    def action_unschedule_posts(self, request, queryset):
        queryset.update(scheduled=False)

    action_unschedule_posts.short_description = _('Unschedule %(verbose_name_plural)s to publish')


class AutoPostMixin(ModelAdminMixin):
    change_form_template = 'social_networks/admin/change_form.html'

    class Media:
        js = (
            'social_networks/admin/js/autopost.js',
        )
        css = {
            'all': (
                'social_networks/admin/css/autopost.css',
            )
        }

    def has_autopost_permissions(self, request):
        """ Проверка, есть ли права на редактирование автопостинга """
        return request.user.has_perm('social_networks.change_feedpost')

    def get_autopost_text(self, obj):
        raise NotImplementedError

    def get_autopost_url(self, obj):
        return obj.get_absolute_url()

    def get_autopost_form(self, request, obj):
        initial_text = self.get_autopost_text(obj)
        initial_text = unescape(strip_tags(initial_text)).strip()
        initial_text = re_newlines.sub('\n', initial_text)
        initial_text = initial_text[:conf.TEXT_MAX_LENGTH]

        if request.method == 'POST':
            return AutpostForm(
                request.POST,
                request.FILES,
                initial={
                    'networks': conf.ALLOWED_NETWORK_NAMES,
                    'text': initial_text,
                },
                prefix=AUTOPOST_FORM_PREFIX
            )
        else:
            return AutpostForm(
                initial={
                    'networks': conf.ALLOWED_NETWORK_NAMES,
                    'text': initial_text,
                },
                prefix=AUTOPOST_FORM_PREFIX
            )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not add:
            info = self.model._meta.app_label, self.model._meta.model_name
            context.update({
                'has_share_permission': self.has_autopost_permissions(request),
                'share_form': self.get_autopost_form(request, obj),
                'share_form_url': reverse('admin:%s_%s_share' % info, args=(obj.pk,)),
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_urls(self):
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        submit_urls = [
            url(
                r'^(\d+)/share/$',
                self.admin_site.admin_view(self.submit_view),
                name='%s_%s_share' % info
            ),
        ]
        return submit_urls + urls

    def submit_view(self, request, object_id):
        try:
            obj = self.model._default_manager.get(pk=object_id)
        except self.model.DoesNotExist:
            raise Http404

        form = self.get_autopost_form(request, obj)
        if form.is_valid():
            obj_ct = ContentType.objects.get_for_model(obj)
            text = form.cleaned_data.get('text')
            networks = form.cleaned_data.get('networks')
            for network in networks:
                try:
                    post = FeedPost.objects.get(
                        network=network,
                        content_type=obj_ct,
                        object_id=obj.pk,
                    )
                except FeedPost.DoesNotExist:
                    FeedPost.objects.create(
                        network=network,
                        url=request.build_absolute_uri(self.get_autopost_url(obj)),
                        text=text,

                        content_type=obj_ct,
                        object_id=obj.pk,
                    )
                else:
                    if post.scheduled:
                        # обновляем данные
                        post.url = request.build_absolute_uri(self.get_autopost_url(obj))
                        post.text = text
                        post.save()

            return JsonResponse({})
        else:
            return JsonResponse({
                'errors': form.errors
            }, status=400)
