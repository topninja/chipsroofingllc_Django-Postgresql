import os
from django.conf import settings
from datetime import datetime, timedelta
from django.core.management import call_command
from project import celery_app


@celery_app.task
def make_backup(max_count=None):
    """
        Создание бэкапа и удаление старых бэкапов,
        если общее кол-во файлов больше max_count
    """
    if not os.path.isdir(settings.BACKUP_ROOT):
        return

    call_command('zipdata', settings.BACKUP_ROOT)

    if max_count is None:
        return

    if isinstance(max_count, int) and max_count > 1:
        files = []
        for file in reversed(sorted(os.listdir(settings.BACKUP_ROOT))):
            absfile = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))
            if os.path.isfile(absfile) and absfile.endswith('.zip'):
                files.append(absfile)

        if len(files) > max_count:
            for old_file in files[max_count:]:
                try:
                    os.unlink(old_file)
                except (FileNotFoundError, PermissionError):
                    pass


@celery_app.task
def clean_admin_log(days=180):
    """
        Удаление записей лога, старее двух месяцев назад
    """
    from admin_log.models import LogEntry
    since_date = datetime.now() - timedelta(days=days)
    LogEntry.objects.filter(action_time__lt=since_date).delete()
