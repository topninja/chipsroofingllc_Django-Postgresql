from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from apps.std_page.models import StdPage
from attachable_blocks.models import AttachableBlock


class TestimonialsPageConfig(SingletonModel, StdPage):
    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Settings')

    def get_absolute_url(self):
        return resolve_url('testimonials:index')

    def __str__(self):
        return ugettext('Testimonials page')


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Testimonials(models.Model):
    config = models.ForeignKey(TestimonialsPageConfig, related_name='testimonials', default=True)

    title = models.CharField(_('header'), max_length=128, blank=True)
    description = models.TextField(_('description'), blank=True)
    star = IntegerRangeField(min_value=1, max_value=5)

    visible = models.BooleanField(_('visible'), default=True)
    sort_order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _('Testimonials')

    def __str__(self):
        return self.title


class TestimonialsBlock(AttachableBlock):
    BLOCK_VIEW = 'testimonials.views.testimonials_block_render'
    header = models.CharField(_('header'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('Testimonials block')
        verbose_name_plural = _('Testimonials block')
