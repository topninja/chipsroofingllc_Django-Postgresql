from django.dispatch import Signal

robokassa_success = Signal(providing_args=['invoice', 'request', 'extra'])
