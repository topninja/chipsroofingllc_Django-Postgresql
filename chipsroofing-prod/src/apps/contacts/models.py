from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from attachable_blocks.models import AttachableBlock
from google_maps.fields import GoogleCoordsField


class ContactsConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=128)
    license = models.CharField(_('license'), max_length=128)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('contacts:index')

    def __str__(self):
        return self.header


class Address(models.Model):
    """ Адрес """
    city = models.CharField(_('city'), max_length=255)
    address = models.CharField(_('address'), max_length=255)
    region = models.CharField(_('region'), max_length=64, blank=True)
    zip = models.CharField(_('zip'), max_length=32, blank=True)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    email = models.EmailField(_('e-mail'), blank=True)
    fax = models.CharField(_('fax'), max_length=255, blank=True)
    url = models.URLField(_('directions link'), blank=True)
    coords = GoogleCoordsField(_('coords'), blank=True)

    sort_order = models.PositiveIntegerField(_('order'))
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        ordering = ('sort_order',)

    def __str__(self):
        return self.address


class NotificationReceiver(models.Model):
    """ Получатели писем с информацией о отправленных сообщениях """
    config = models.ForeignKey(ContactsConfig, related_name='receivers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('notification receiver')
        verbose_name_plural = _('notification receivers')

    def __str__(self):
        return self.email


class Message(models.Model):
    """ Сообщение """
    TYPE_MESSAGE = (
        ('btn-popup-contact', 'Contact Us'),
        ('btn-popup-estimate', 'Estimate'),
    )

    type_message = models.CharField(_('type message'), choices=TYPE_MESSAGE, default='contact', max_length=128)
    name = models.CharField(_('name'), max_length=128)
    email = models.EmailField(_('e-mail'), blank=True)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    message = models.TextField(_('message'), max_length=2048)
    date = models.DateTimeField(_('date sent'), default=now, editable=False)
    referer = models.CharField(_('from page'), max_length=512, blank=True, editable=False)

    class Meta:
        default_permissions = ('delete',)
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ('-date',)

    def __str__(self):
        return self.name


class ContactBlock(AttachableBlock):
    """ Подключаемый блок с контактной формой """
    BLOCK_VIEW = 'contacts.views.contact_block_render'

    header = models.CharField(_('header'), max_length=128, blank=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('Contact block')
        verbose_name_plural = _('Contact blocks')
