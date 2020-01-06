from ipware.ip import get_ip
from urllib.parse import unquote_plus
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    STATUS_INFO = 1
    STATUS_SUCCESS = 2
    STATUS_ERROR = 3
    STATUS_EXCEPTION = 4
    STATUSES = (
        (STATUS_INFO, _('Info')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_ERROR, _('Error')),
        (STATUS_EXCEPTION, _('Exception')),
    )

    inv_id = models.BigIntegerField(_('invoice'), blank=True, null=True)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUSES)
    msg_body = models.TextField(_('message'))
    request_get = models.TextField(_('GET'))
    request_post = models.TextField(_('POST'))
    request_ip = models.GenericIPAddressField(_('IP'))
    created = models.DateTimeField(_('create date'), default=now, editable=False)

    class Meta:
        default_permissions = ('delete', )
        verbose_name = _('log message')
        verbose_name_plural = _('log messages')
        ordering = ('-created', )

    def __str__(self):
        status = dict(self.STATUSES).get(self.status)
        return '[%s] %s' % (status, self.msg_body)

    @classmethod
    def create(cls, request, body, inv_id=None, status=None):
        return cls.objects.create(
            inv_id=inv_id,
            status=status,
            msg_body=body,
            request_get=unquote_plus(request.GET.urlencode()),
            request_post=unquote_plus(request.POST.urlencode()),
            request_ip=get_ip(request),
        )

    @classmethod
    def message(cls, request, body, inv_id=None):
        return cls.create(request, body, inv_id, status=cls.STATUS_INFO)

    @classmethod
    def success(cls, request, body, inv_id=None):
        return cls.create(request, body, inv_id, status=cls.STATUS_SUCCESS)

    @classmethod
    def error(cls, request, body, inv_id=None):
        return cls.create(request, body, inv_id, status=cls.STATUS_ERROR)

    @classmethod
    def exception(cls, request, body, inv_id=None):
        return cls.create(request, body, inv_id, status=cls.STATUS_EXCEPTION)
