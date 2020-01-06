from django.dispatch import Signal

paypal_success = Signal(providing_args=[
    'request',
    'invoice', 'items', 'amount', 'description', 'item_number', 'quantity',
    'custom',
])
