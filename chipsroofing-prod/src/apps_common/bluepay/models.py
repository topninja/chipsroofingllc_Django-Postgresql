from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    STATUS_MESSAGE = 1
    STATUS_SUCCESS = 2
    STATUS_ERROR = 3
    STATUS_EXCEPTION = 4
    STATUSES = (
        (STATUS_MESSAGE, _('Message')),
        (STATUS_SUCCESS, _('Success')),
        (STATUS_ERROR, _('Error')),
        (STATUS_EXCEPTION, _('Exception')),
    )

    inv_id = models.PositiveIntegerField(_('InvId'), blank=True, null=True)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUSES)
    message = models.TextField(_('message'))
    request = models.TextField(_('request'))
    created = models.DateTimeField(_('create date'), default=now, editable=False)

    class Meta:
        default_permissions = ('delete', )
        verbose_name = _('log message')
        verbose_name_plural = _('log messages')
        ordering = ('-created', )

    def __str__(self):
        status = dict(self.STATUSES).get(self.status)
        return '[%s] %s' % (status, self.message)

