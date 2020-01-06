from django.db import models
from django.core import checks
from libs.autocomplete.widgets import AutocompleteWidget
from .models import AttachableBlock


def blocks_format_item(obj):
    return {
        'id': obj.id,
        'text': obj.label
    }


class AttachableBlockField(models.ForeignKey):

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self.check_block_model(**kwargs))
        return errors

    def check_block_model(self, **kwargs):
        if not issubclass(self.rel.to, AttachableBlock):
            return [
                checks.Error(
                    'reference must be on AttachableBlock subclass',
                    obj=self,
                )
            ]
        else:
            return []

    def formfield(self, **kwargs):
        defaults = {
            'widget': AutocompleteWidget(
                expressions='label__icontains',
                format_item=blocks_format_item,
            )
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
