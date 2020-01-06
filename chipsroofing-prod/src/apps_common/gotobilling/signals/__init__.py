from django.dispatch import Signal

gotobilling_success = Signal(providing_args=['invoice', 'request'])
gotobilling_error = Signal(providing_args=['invoice', 'request', 'code', 'reason'])
