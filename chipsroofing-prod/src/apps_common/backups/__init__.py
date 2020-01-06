"""
    Модуль бэкапов данных.

    Зависит от:
        libs.download

    Установка:
        settings.py:

            INSTALLED_APPS = (
                ...
                'backups',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'backups',
                    'icon': 'icon-hdd',
                },
                ...
            }

            BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

"""

default_app_config = 'backups.apps.Config'
