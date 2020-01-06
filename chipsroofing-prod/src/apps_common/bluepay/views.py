from django.shortcuts import redirect
from .models import Log
from .forms import ResultForm
from .signals import bluepay_success, bluepay_error
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
        inv_id=data.get('INVOICE_ID'),
        status=Log.STATUS_MESSAGE,
        request=urlencoded,
    )

    form = ResultForm(data)
    if form.is_valid():
        invoice = form.cleaned_data['INVOICE_ID']
        try:
            invoice = int(invoice)
        except (TypeError, ValueError):
            invoice = None

        result_name = form.cleaned_data['Result']
        if result_name == ResultForm.RESULT_APPROVED:
            # ------------------------------
            #   Approved
            # ------------------------------
            try:
                bluepay_success.send(
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
            reason = form.cleaned_data['MESSAGE']
            try:
                bluepay_error.send(
                    sender=Log,
                    invoice=invoice,
                    request=request,
                    code=result_name,
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
            inv_id=data.get('INVOICE_ID'),
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
