from django.apps import apps
from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

DEFAULT_PERMS = ('add', 'change', 'delete')


class Command(BaseCommand):
    help = _('Clean unused default permissions')

    def handle(self, *args, **options):

        for model in apps.get_models():
            allowed_perms = model._meta.default_permissions
            if allowed_perms == DEFAULT_PERMS:
                continue

            perms_to_remove = tuple(
                '%s_%s' % (default_perm, model._meta.model_name)
                for default_perm in DEFAULT_PERMS
                if default_perm not in allowed_perms
            )

            ct = ContentType.objects.get_for_model(model)
            for perm in Permission.objects.filter(content_type=ct, codename__in=perms_to_remove):
                print(perm)
                perm.delete()

        print('Done')

