from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from libs.range_field import RangeField


class RatingVote(models.Model):
    ip = models.GenericIPAddressField(_('ip'))
    rating = RangeField(_('vote'), min_value=1, max_value=5)
    date = models.DateTimeField(_('date'), default=now, db_index=True)

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        ordering = ('-date', )

    def __str__(self):
        return '%s - %d stars' % (self.ip, self.rating)
