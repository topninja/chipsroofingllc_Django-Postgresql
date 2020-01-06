from django.db import models
from django.core import checks
from django.utils.timezone import now
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from model_utils.managers import InheritanceQuerySetMixin
from .utils import get_model_by_ct, get_block_view


class AttachableBlockQuerySet(InheritanceQuerySetMixin, models.QuerySet):
    pass


class AttachableBlock(models.Model):
    """ Базовый класс блоков """
    BLOCK_VIEW = ''

    content_type = models.ForeignKey(ContentType, null=True, related_name='+', editable=False)
    label = models.CharField(_('label'), max_length=128, help_text=_('For inner use'))
    visible = models.BooleanField(_('visible'), default=True)
    created = models.DateTimeField(_('create date'), editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    objects = AttachableBlockQuerySet.as_manager()

    class Meta:
        default_permissions = ()
        verbose_name = _('attachable block')
        verbose_name_plural = _('attachable blocks')
        ordering = ('label', )

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = now()

        if not self.content_type:
            if self.__class__ != AttachableBlock:
                self.content_type = ContentType.objects.get_for_model(self)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_views(**kwargs))
        return errors

    @classmethod
    def _check_views(cls, **kwargs):
        if cls is AttachableBlock:
            return []

        if not cls.BLOCK_VIEW:
            return [
                checks.Error(
                    'BLOCK_VIEW is required',
                    obj=cls
                )
            ]
        elif not get_block_view(cls):
            return [
                checks.Error(
                    'BLOCK_VIEW not found',
                    obj=cls
                )
            ]
        else:
            return []


class AttachableReference(models.Model):
    """
        Связь экземпляра блока с экземпляром страницы
    """
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.IntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    block_ct = models.ForeignKey(ContentType, null=True, related_name='+')
    block = models.ForeignKey(AttachableBlock, verbose_name=_('block'), related_name='references')
    ajax = models.BooleanField(_('AJAX'), default=False,
        help_text=_('load block via AJAX')
    )

    set_name = models.CharField(_('set name'), max_length=32, default='default')
    sort_order = models.IntegerField(_('sort order'), default=0)

    class Meta:
        verbose_name = _('attached block')
        verbose_name_plural = _('attached blocks')
        ordering = ('set_name', 'sort_order')
        index_together = (('content_type', 'object_id', 'set_name'), )

    def __str__(self):
        block_model = get_model_by_ct(self.block_ct_id)
        block_name = block_model._meta.verbose_name or 'Undefined'

        instance = '%s.%s (#%s)' % (
            self.content_type.app_label,
            self.content_type.model,
            self.object_id
        )
        return '%s (%s) → %s' % (self.block, block_name, instance)

    @classmethod
    def get_for(cls, instance, set_name=None):
        """
            Получение объектов ссылок на видимые блоки для сущности
        """
        ct = ContentType.objects.get_for_model(instance)
        query = models.Q(
            content_type=ct,
            object_id=instance.pk,
            block__visible=True,
        )

        if set_name is not None:
            query &= models.Q(set_name=set_name)

        return cls.objects.filter(query)

    @classmethod
    def create(cls, instance, block, set_name='default', **kwargs):
        """
            Добавление ссылки на блок для сущности.
            Нигде не используется. Предназначен для массовой
            привязки блока через консоль.
        """
        if not isinstance(block, AttachableBlock):
            raise TypeError(_('block must be an instance of AttachableBlock'))

        if not isinstance(instance, models.Model):
            raise TypeError(_('instance must be an instance of Model'))

        # По умолчанию, добавляем в конец
        if 'sort_order' not in kwargs:
            kwargs['sort_order'] = cls.get_for(
                instance,
                set_name=set_name,
            ).aggregate(
                max=Coalesce(models.Max('sort_order'), 0) + 1
            )['max'] + 1

        ct = ContentType.objects.get_for_model(instance)
        block_ct = ContentType.objects.get_for_model(block)
        return cls.objects.create(
            content_type=ct,
            object_id=instance.pk,
            block_ct=block_ct,
            block=block,
            set_name=set_name,
            **kwargs
        )
