from django.dispatch import Signal

payeezy_success = Signal(providing_args=['invoice', 'request'])
payeezy_error = Signal(providing_args=['invoice', 'request', 'code', 'reason', 'subreason'])
