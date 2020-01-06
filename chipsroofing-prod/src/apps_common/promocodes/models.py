from django.db import models
from django.utils.timezone import now
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from solo.models import SingletonModel
from .strategies import BaseStrategy, STRATEGIES, STRATEGY_CHOICES
from . import exceptions


class PromoSettings(SingletonModel):

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')


class PromoCode(models.Model):
    title = models.CharField(_('title'), max_length=128)
    code = models.CharField(_('code'), max_length=24, validators=[MinLengthValidator(4)], unique=True)
    strategy_name = models.CharField(_('action'), max_length=64, choices=STRATEGY_CHOICES)
    parameter = models.CharField(_('parameter'), max_length=32, blank=True, default='0')

    redemption_limit = models.PositiveIntegerField(_('redemption limit'), default=1,
        help_text=_('zero sets the limit to unlimited')
    )
    start_date = models.DateTimeField(_('start time'), blank=True, null=True)
    end_date = models.DateTimeField(_('end time'), blank=True, null=True)

    self_created = models.BooleanField(_('self-created'), default=False)
    created = models.DateTimeField(_('created on'), default=now, editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('promo code')
        verbose_name_plural = _('promo codes')
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    @property
    def times_used(self):
        """ Сколько раз использован промокод """
        return self.references.filter(applied=True).count()

    @property
    def strategy(self) -> BaseStrategy:
        """ Получение класса стратегии """
        return STRATEGIES[self.strategy_name]

    @property
    def short_description(self):
        """ Делегируемый метод для получения краткого описания стратегии промокода """
        return self.strategy.short_description(self)

    @property
    def full_description(self):
        """ Делегируемый метод для получения полного описания стратегии промокода """
        return self.strategy.full_description(self)

    def calculate(self, *args, **kwargs):
        """ Делегируемый метод для рассчета размера скидки """
        return self.strategy.calculate(self, *args, **kwargs)

    def validate(self, *args, **kwargs):
        """
            Проверка возможности использования промокода.
            ВНИМАНИЕ! Потоконебезопасно! Если следом идёт добавление PromoCodeReference,
            то это должно происходить внутри блокировки таблицы.
        """
        now_date = now()

        if self.start_date and now_date < self.start_date:
            raise exceptions.PromoCodeExpiredError(_('This promo code has expired'))

        if self.end_date and now_date > self.end_date:
            raise exceptions.PromoCodeExpiredError(_('This promo code has expired'))

        if self.redemption_limit and (self.times_used >= self.redemption_limit):
            raise exceptions.PromoCodeLimitReachedError(
                _('This promo code has reached it\'s redemption limit')
            )

        # дополнительная валидация стратегии
        self.strategy.validate(*args, **kwargs)


class PromoCodeReference(models.Model):
    promocode = models.ForeignKey(PromoCode, verbose_name=_('promo code'), related_name='references')

    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    applied = models.BooleanField(_('applied'), default=False, editable=False)
    created = models.DateTimeField(_('created on'), default=now, editable=False)

    class Meta:
        verbose_name = _('promo code reference')
        verbose_name_plural = _('promo code references')
        ordering = ('-created',)
        unique_together = ('promocode', 'content_type', 'object_id')

    def __str__(self):
        instance = '%s.%s (#%s)' % (
            self.content_type.app_label,
            self.content_type.model,
            self.object_id
        )
        return '%s → %s' % (self.promocode, instance)

    @property
    def short_description(self):
        """ Делегируемый метод для получения краткого описания стратегии промокода """
        return self.promocode.short_description

    @property
    def full_description(self):
        """ Делегируемый метод для получения полного описания стратегии промокода """
        return self.promocode.full_description

    def calculate(self, *args, **kwargs):
        """ Делегируемый метод для рассчета размера скидки """
        return self.promocode.calculate(*args, **kwargs)
