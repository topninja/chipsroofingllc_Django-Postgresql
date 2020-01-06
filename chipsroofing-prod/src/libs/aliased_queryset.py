from django.db import models


class AliasedQuerySetMixin:
    """
        QuerySet с возможностью создания алиасов для набора
        параметров фильтрации.

        Заданные параметры работают в методах filter(), get(), exclude()

        Пример:

            class MyQuerySet(AliasedQuerySetMixin, models.QuerySet):
                def aliases(self, qs, kwargs):
                    visible = kwargs.pop('visible', None)
                    if visible is None:
                        pass
                    elif visible:
                        qs &= models.Q(date__gt=now())
                    else:
                        qs &= models.Q(date__lte=now())

                    return qs
    """

    def aliases(self, qs, kwargs):
        return qs

    def _filter_or_exclude(self, negate, *args, **kwargs):
        qs = self.aliases(models.Q(), kwargs)
        return super()._filter_or_exclude(negate, qs, *args, **kwargs)
