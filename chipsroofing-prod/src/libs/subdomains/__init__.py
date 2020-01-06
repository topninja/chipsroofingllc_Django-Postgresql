"""
    Модуль, добавляющий в request поле subdomain, содержащее текущий поддомен.
    
    Основной домен берется из Site.domain.
    
    Установка:
        settings.py:
            MIDDLEWARE_CLASSES = (
                ...
                'libs.subdomains.middleware.SubdomainMiddleware',
                ...
            )

"""