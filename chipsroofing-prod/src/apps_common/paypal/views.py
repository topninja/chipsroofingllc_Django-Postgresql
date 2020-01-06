from decimal import Decimal
from urllib.parse import unquote_plus
from requests import post as http_post
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Log
from .forms import PayPalResultForm
from .signals import paypal_success
from . import conf


def _log_errors(errors):
    return '\n'.join(
        '{}: {}'.format(
            key,
            ', '.join(errors_list)
        )
        for key, errors_list in errors.items()
    )


@csrf_exempt
def result(request):
    """ Обработчик результата оплаты """
    data = request.POST
    Log.message(request, 'Webhook: start')

    form = PayPalResultForm(data)
    if not form.is_valid():
        Log.error(request, 'Webhook: invalid form\n{}'.format(
            _log_errors(form.errors),
        ))

    payment_status = form.cleaned_data['payment_status']
    receiver_email = unquote_plus(form.cleaned_data['receiver_email'])
    invoice = form.cleaned_data.get('invoice', '')
    try:
        invoice = int(invoice)
    except (TypeError, ValueError):
        invoice = None

    resp = http_post(conf.FORM_TARGET, 'cmd=_notify-validate&' + request.body.decode())
    if resp.text == 'VERIFIED' and payment_status.lower() == 'completed' and receiver_email.lower() == conf.EMAIL.lower():
        cart = []
        index = 1
        while 'item_number%s' % index in data:
            cart.append({
                'number': data.get('item_number%s' % index),
                'name': data.get('item_name%s' % index),
                'count': int(data.get('quantity%s' % index)),
                'cost': Decimal(data.get('mc_gross_%s' % index)),
            })
            index += 1

        try:
            paypal_success.send(
                sender=Log,
                request=request,
                invoice=invoice,
                items=cart,
                amount=form.cleaned_data['mc_gross'],
                item_number=form.cleaned_data['item_number'],
                quantity=form.cleaned_data['quantity'],
                custom=form.cleaned_data['custom'],
            )
        except Exception as e:
            Log.exception(request, 'Webhook: %s(%s)'.format(
                e.__class__.__name__,
                ', '.join(e.args),
            ))
        else:
            Log.success(request, 'Transaction: success')
    else:
        Log.error(request, 'Webhook: unverified request')

    return HttpResponse('')
