import re
from django.db import models
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from libs.email import absolute_links
from libs.color_field.fields import ColorField
from libs.storages.media_storage import MediaStorage
from .. import api

re_newline_spaces = re.compile(r'[\r \t]*\n[\r \t]*')
re_newlines = re.compile(r'\n{3,}')
re_domain_urls = re.compile(r'(url\()(/[^/])')


class MailerConfig(SingletonModel):
    from_name = models.CharField(_('sender name'), max_length=255, default='John Smith',
        help_text=_('should be your name')
    )
    from_email = models.EmailField(_('sender e-mail'), default='manager@example.com',
        help_text=_('must be valid and actually exists')
    )

    bg_color = ColorField(_('background color'), blank=True, default='#BDC3C7')
    bg_image = models.ImageField(_('background image'), blank=True,
        storage=MediaStorage('mailerlite/campaigns')
    )

    footer_text = models.TextField(_('text'), blank=True)
    website = models.URLField(_('website address'), max_length=255)
    contact_email = models.EmailField(_('contact email'), default='admin@example.com')

    import_groups_date = models.DateTimeField(default=now, editable=False)
    import_campaigns_date = models.DateTimeField(default=now, editable=False)
    import_subscribers_date = models.DateTimeField(default=now, editable=False)
    export_groups_date = models.DateTimeField(default=now, editable=False)
    export_campaigns_date = models.DateTimeField(default=now, editable=False)
    export_subscribers_date = models.DateTimeField(default=now, editable=False)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def __str__(self):
        return ugettext('Settings')


class Group(models.Model):
    name = models.CharField(_('name'), max_length=255)
    subscribable = models.BooleanField(_('subscribable'), default=False)

    # статус
    remote_id = models.BigIntegerField(_('ID in Mailerlite'), default=0, db_index=True)
    need_export = models.BooleanField(_('need export'), default=False)

    # статистика
    total = models.PositiveIntegerField(_('total'), default=0, editable=False)
    active = models.PositiveIntegerField(_('active'), default=0, editable=False)
    bounced = models.PositiveIntegerField(_('bounced'), default=0, editable=False)
    unsubscribed = models.PositiveIntegerField(_('unsubscribed'), default=0, editable=False)
    sent = models.PositiveIntegerField(_('sent'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicked'), default=0, editable=False)

    # дата и время создания/изменения удаленного объекта
    date_created = models.DateTimeField(_('date created'), null=True, editable=False)
    date_updated = models.DateTimeField(_('date updated'), null=True, editable=False)

    # дата и время создания/изменения локального объекта
    created = models.DateTimeField(_('created'), default=now, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('list')
        verbose_name_plural = _('lists')
        ordering = ('-date_created',)

    def __str__(self):
        return self.name

    def save(self, *args, need_export=True, **kwargs):
        self.need_export = need_export
        super().save(*args, **kwargs)


class BaseCampaign(models.Model):
    STATUS_CHOICES = (
        (api.campaings.STATUS_DRAFT, _('Draft')),
        (api.campaings.STATUS_OUTBOX, _('Outbox')),
        (api.campaings.STATUS_SENT, _('Sent')),
    )

    # переопределение отправителя
    from_name = models.CharField(_('sender name'), max_length=255, blank=True)
    from_email = models.EmailField(_('sender e-mail'), blank=True)

    subject = models.CharField(_('subject'), max_length=255)
    groups = models.ManyToManyField(Group, verbose_name=_('recipients'))

    # статус
    status = models.CharField(_('status'), max_length=16, choices=STATUS_CHOICES, default=api.campaings.STATUS_DRAFT)
    export_allowed = models.BooleanField(_('export allowed'), default=False)
    remote_id = models.BigIntegerField(_('ID in Mailerlite'), default=0, db_index=True)

    # статистика
    total_recipients = models.PositiveIntegerField(_('total recipients'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicked'), default=0, editable=False)

    # дата и время создания и отправки удаленного объекта
    date_created = models.DateTimeField(_('date created'), null=True, editable=False)
    date_send = models.DateTimeField(_('date send'), null=True, editable=False)

    # дата и время создания/изменения локального объекта
    created = models.DateTimeField(_('created'), default=now, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        default_permissions = ('add', 'change')
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = ('-date_created',)
        abstract = True

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.from_email or not self.from_name:
            config = MailerConfig.get_solo()
            self.from_name = config.from_name
            self.from_email = config.from_email
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mailerlite:preview', kwargs={'campaign_id': self.pk})

    @property
    def test_subject(self):
        subject = self.subject.replace('{$name}', 'John')
        subject = subject.replace('{$last_name}', 'Smith')
        return subject

    def render_html(self, request=None, **kwargs):
        raise NotImplementedError

    def final_html(self, request=None, scheme='//', **kwargs):
        """ Отформатированный вывод для сервиса Mailerlite """
        content = self.render_html(request, **kwargs)
        content = content.replace('url(//', 'url(http://')
        content = absolute_links(content, scheme=scheme, request=request)
        site = get_current_site(request)
        content = re_domain_urls.sub('\\1{}{}\\2'.format(scheme, site.domain), content)
        return content

    def render_plain(self, request=None, **kwargs):
        raise NotImplementedError

    def final_plain(self, request=None, **kwargs):
        """ Отформатированный вывод для сервиса Mailerlite """
        content = self.render_plain(request, **kwargs)
        content = re_newline_spaces.sub('\n', content)
        content = re_newlines.sub('\n\n', content)
        return content.strip()


class Subscriber(models.Model):
    STATUS_CHOICES = (
        (api.subscribers.STATUS_ACTIVE, _('Active')),
        (api.subscribers.STATUS_UNCONFIRMED, _('Unconfirmed')),
        (api.subscribers.STATUS_UNSUBSCRIBED, _('Unsubscribed')),
        (api.subscribers.STATUS_BOUNCED, _('Bounced')),
        (api.subscribers.STATUS_JUNK, _('Junk')),
    )

    groups = models.ManyToManyField(Group, verbose_name=_('groups'))
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    company = models.CharField(_('company'), max_length=255, blank=True)

    # статус
    status = models.CharField(_('status'), max_length=32, choices=STATUS_CHOICES, default=api.subscribers.STATUS_ACTIVE)
    remote_id = models.BigIntegerField(_('ID in Mailerlite'), default=0, db_index=True)
    need_export = models.BooleanField(_('need export'), default=False)

    # статистика
    sent = models.PositiveIntegerField(_('sent'), default=0, editable=False)
    opened = models.PositiveIntegerField(_('opened'), default=0, editable=False)
    clicked = models.PositiveIntegerField(_('clicked'), default=0, editable=False)

    # дата и время создания и отправки удаленного объекта
    date_created = models.DateTimeField(_('date subscribed'), null=True, editable=False)
    date_subscribe = models.DateTimeField(_('date subscribe'), null=True, editable=False)
    date_unsubscribe = models.DateTimeField(_('date unsubscribe'), null=True, editable=False)
    date_updated = models.DateTimeField(_('date updated'), null=True, editable=False)

    # дата и время создания/изменения локального объекта
    created = models.DateTimeField(_('created'), default=now, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        default_permissions = ('add', 'change')
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')
        ordering = ('-date_created', 'id')

    def __str__(self):
        return self.email

    def clean(self):
        self.email = self.email.lower()

    def save(self, *args, need_export=True, **kwargs):
        self.need_export = need_export
        super().save(*args, **kwargs)
