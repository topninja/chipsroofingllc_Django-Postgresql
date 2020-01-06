from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from ckeditor.fields import CKEditorUploadField
from social_networks.models import SocialLinks
from .base import MailerConfig, BaseCampaign
from .. import conf


class RegularCampaign(BaseCampaign):
    HTML_TEMPLATE = 'mailerlite/regular/html.html'
    PLAIN_TEMPLATE = 'mailerlite/regular/plain.html'

    text = CKEditorUploadField(_('text'), height=350, editor_options=conf.CKEDITOR_CONFIG)

    def render_html(self, request=None, **kwargs):
        site = get_current_site(request)
        return loader.render_to_string(self.HTML_TEMPLATE, {
            'domain': site.domain,
            'config': MailerConfig.get_solo(),
            'socials': SocialLinks.get_solo(),
            'campaign': self,
        }, request=request)

    def render_plain(self, request=None, **kwargs):
        site = get_current_site(request)
        return loader.render_to_string(self.PLAIN_TEMPLATE, {
            'domain': site.domain,
            'config': MailerConfig.get_solo(),
            'socials': SocialLinks.get_solo(),
            'campaign': self,
        }, request=request)
