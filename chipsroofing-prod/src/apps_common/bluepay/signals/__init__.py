from django.dispatch import Signal

bluepay_success = Signal(providing_args=['invoice', 'request'])
bluepay_error = Signal(providing_args=['invoice', 'request', 'code', 'reason'])
