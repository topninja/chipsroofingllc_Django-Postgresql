from django.db import models
from django.utils.translation import ugettext_lazy as _


class Backup(models.Model):
    class Meta:
        managed = False
        verbose_name = _('backup')
        verbose_name_plural = _('backups')
        default_permissions = ()
