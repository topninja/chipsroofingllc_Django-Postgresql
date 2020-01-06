from django.dispatch import Signal

authorizenet_success = Signal(providing_args=[
    'request', 'code', 'reason', 'reasonText',
    'invoice', 'amount', 'description'
])
