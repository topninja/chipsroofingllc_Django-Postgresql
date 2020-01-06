from django.db import models
from django.utils.translation import ugettext_lazy as _


class Breadcrumbs:
    def __init__(self):
        self.crumbs = [{
            'title': _('HOME'),
            'url': '/',
        }]
        # self.crumbs = []

    def __bool__(self):
        return bool(self.crumbs)

    def __iter__(self):
        return iter(self.crumbs)

    def add(self, title, url='', **kwargs):
        if isinstance(title, models.Model):
            self.crumbs.append(dict(
                title=str(title),
                url=title.get_absolute_url(),
                **kwargs
            ))
        else:
            self.crumbs.append(dict(
                title=title,
                url=url,
                **kwargs
            ))
