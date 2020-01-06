import re
import hmac
import json
from hashlib import sha512
from decimal import Decimal
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Log
from .signals import authorizenet_success
from . import conf
from . import api

re_webhook_signature = re.compile(r'sha512=(\w{128})')


def _parse_webhook(request):
    """
        Валидация хука
    """
    signature = request.META.get('HTTP_X_ANET_SIGNATURE', '')
    if not signature:
        Log.error(request, 'Webhook: empty signature header')
        return

    match = re_webhook_signature.fullmatch(signature)
    if not match:
        Log.error(request, 'Webhook: invalid signature %r' % signature)
        return

    header_hmac = match.group(1)
    body_hmac = hmac.new(conf.SIGNATURE_KEY.encode(), request.body, digestmod=sha512).hexdigest()
    if body_hmac.upper() != header_hmac.upper():
        Log.error(request, 'Webhook: signature mismatch')
        return

    data = json.loads(request.body.decode())
    event_type = data.get('eventType', '')
    if not event_type:
        Log.error(request, 'Webhook: unknown eventType')
        return

    # Остальные типы
    if event_type != 'net.authorize.payment.authcapture.created':
        Log.message(request, 'Webhook: %s' % event_type)
        return

    return data


def _parse_transaction(request, trans_id):
    details = api.get_transaction(trans_id)
    if details is None:
        Log.error(request, 'Transaction: not found')
        return

    if details.transactionType != 'authCaptureTransaction':
        Log.error(request, 'Transaction: transactionType mismatch')
        return

    if details.responseCode != 1:
        Log.error(request, 'Transaction: bad transaction status "%s (code: %s; reason: %s)"' % (
            details.responseReasonDescription,
            details.responseCode,
            details.responseReasonCode,
        ))
        return

    return details


@csrf_exempt
def webhook(request):
    """
        Обработка Webhook
    """
    Log.message(request, 'Webhook: start')

    data = _parse_webhook(request)
    if data is None:
        return HttpResponse()

    try:
        trans_id = data['payload']['id']
    except AttributeError:
        Log.error(request, 'Webhook: transaction ID not found')
        return HttpResponse()

    # Получение транзакции
    details = _parse_transaction(request, trans_id)
    if data is None:
        return HttpResponse()

    # Собираем информацию
    try:
        amount = Decimal(str(details.authAmount))
    except Exception:
        Log.exception(request, 'Transaction: invalid amount "%s"' % details.authAmount)
        return HttpResponse()

    try:
        invoice = int(details.order.invoiceNumber)
    except Exception:
        Log.exception(request, 'Transaction: invalid invoice "%s"' % details.order.invoiceNumber)
        return HttpResponse()

    try:
        description = str(details.order.description)
    except Exception:
        Log.exception(request, 'Transaction: invalid description "%s"' % details.order.description)
        return HttpResponse()

    try:
        authorizenet_success.send(
            sender=Log,
            request=request,
            code=details.responseCode,
            reason=details.responseReasonCode,
            reasonText=details.responseReasonDescription,
            invoice=invoice,
            amount=amount,
            description=description,
        )
    except Exception as e:
        Log.exception(request, 'Transaction: %s(%s)' % (
            e.__class__.__name__,
            ', '.join(e.args),
        ), inv_id=invoice)
    else:
        Log.success(request, 'Transaction: success', inv_id=invoice)

    return HttpResponse()
