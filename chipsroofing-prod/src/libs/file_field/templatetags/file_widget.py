import os
from django.template import Library

register = Library()


@register.filter
def basename(value):
    return os.path.basename(value)
