from django.shortcuts import redirect
from .models import Log
from .forms import GotobillingResultForm
from .signals import gotobilling_success, gotobilling_error
from . import conf


def _log_errors(errors):
    return '\n'.join(
        '{}: {}'.format(
            key,
            ', '.join(errors_list)
        )
        for key, errors_list in errors.items()
    )


def result(request):
    """ Обработчик результата оплаты """
    data = request.GET
    urlencoded = data.urlencode().replace('&', '\n')

    # log data
    Log.objects.create(
        inv_id=data.get('x_invoice_num'),
        status=Log.STATUS_MESSAGE,
        request=urlencoded,
    )

    form = GotobillingResultForm(data)
    if form.is_valid():
        invoice = form.cleaned_data['x_invoice_num']
        try:
            invoice = int(invoice)
        except (TypeError, ValueError):
            invoice = None

        response_code = form.cleaned_data['x_response_code']
        if response_code == GotobillingResultForm.RESPONSE_CODE_APPROVED:
            # ------------------------------
            #   Approved
            # ------------------------------
            try:
                gotobilling_success.send(
                    sender=Log,
                    invoice=invoice,
                    request=request,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=invoice,
                    status=Log.STATUS_EXCEPTION,
                    request=urlencoded,
                    message='Signal exception:\n{}: {}'.format(
                        e.__class__.__name__,
                        ', '.join(e.args),
                    )
                )
            else:
                # log success
                Log.objects.create(
                    inv_id=invoice,
                    status=Log.STATUS_SUCCESS,
                    request=urlencoded,
                )
        else:
            # ------------------------------
            #   Declined или Error
            # ------------------------------
            reason = form.cleaned_data['x_response_reason_text']
            try:
                gotobilling_error.send(
                    sender=Log,
                    invoice=invoice,
                    request=request,
                    code=response_code,
                    reason=reason,
                )
            except Exception as e:
                # log exception
                Log.objects.create(
                    inv_id=invoice,
                    status=Log.STATUS_EXCEPTION,
                    request=urlencoded,
                    message='Signal exception:\n{}: {}'.format(
                        e.__class__.__name__,
                        ', '.join(e.args),
                    )
                )
            else:
                # log fail
                Log.objects.create(
                    inv_id=invoice,
                    status=Log.STATUS_ERROR,
                    request=urlencoded,
                    message=reason,
                )

            return redirect(conf.FAIL_URL)
    else:
        # log form error
        Log.objects.create(
            inv_id=data.get('x_invoice_num'),
            status=Log.STATUS_ERROR,
            request=urlencoded,
            message='Invalid form:\n{}'.format(
                _log_errors(form.errors),
            )
        )

    # Показываем Success даже если форма не валидна,
    # чтобы не пугать пользователя, если, например,
    # хэш рассчитывается неправильно
    return redirect(conf.SUCCESS_URL)
