from django.utils import timezone
from django.template import Library
from django.utils.formats import date_format
from django.utils.translation import ugettext as _, ungettext_lazy

register = Library()


@register.filter(expects_localtime=True)
def shortdate(value):
    now = timezone.template_localtime(timezone.now())
    diff = now - value

    if diff < timezone.timedelta():
        return date_format(value, "DATE_FORMAT")
    elif diff.days < 1:
        return _('today')
    elif diff.days < 2:
        return _('yesterday')
    elif diff.days < 30:
        return ungettext_lazy('%d day ago', '%d days ago') % diff.days
    else:
        months = diff.days // 30
        if months <= 6:
            return ungettext_lazy('a month ago', '%d months ago') % months
        else:
            return date_format(value, "DATE_FORMAT")
