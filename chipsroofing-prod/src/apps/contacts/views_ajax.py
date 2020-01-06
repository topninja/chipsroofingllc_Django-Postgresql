from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from libs.email import send_template
from .models import ContactsConfig, NotificationReceiver
from .forms import ContactForm, FreeEstimateForm


class ContactView(AjaxViewMixin, View):
    def get(self, request):
        config = ContactsConfig.get_solo()
        form = ContactForm()
        return self.json_response({
            'form': self.render_to_string('contacts/popups/contact_form.html', {
                'config': config,
                'form': form,
            }),
        })

    def post(self, request):
        config = ContactsConfig.get_solo()
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid() and self.request.recaptcha_is_valid:
            message = form.save(commit=False)
            referer = request.POST.get('referer')
            message.referer = escape(referer)
            message.save()

            receivers = NotificationReceiver.objects.all().values_list('email', flat=True)
            send_template(request, receivers,
                          subject=_('Message from {domain}'),
                          template='contacts/mails/message.html',
                          context={
                              'message': message,
                          }
                          )

            return self.json_response({
                'success_message': self.render_to_string('contacts/popups/contact_success.html', {
                    'config': config,
                })
            })
        else:
            return self.json_error({
                'errors': form.error_dict_full,
                'recaptcha_is_valid': self.request.recaptcha_is_valid,
                'form': self.render_to_string('contacts/popups/contact_form.html', {
                    'config': config,
                    'form': form,
                }),
            })


class FreeEstimateView(AjaxViewMixin, View):
    def get(self, request):
        config = ContactsConfig.get_solo()
        form_estimate = FreeEstimateForm()
        return self.json_response({
            'form': self.render_to_string('contacts/popups/estimate_form.html', {
                'config': config,
                'form': form_estimate,
            }),
        })

    def post(self, request):
        config = ContactsConfig.get_solo()
        form_estimate = FreeEstimateForm(request.POST, request.FILES)
        if form_estimate.is_valid() and self.request.recaptcha_is_valid:
            message = form_estimate.save(commit=False)
            referer = request.POST.get('referer')
            message.referer = escape(referer)
            message.save()

            receivers = NotificationReceiver.objects.all().values_list('email', flat=True)
            send_template(request, receivers,
                          subject=_('Message from {domain}'),
                          template='contacts/mails/message.html',
                          context={
                              'message': message,
                          }
                          )

            return self.json_response({
                'success_message': self.render_to_string('contacts/popups/contact_success.html', {
                    'config': config,
                })
            })
        else:
            return self.json_error({
                'errors': form_estimate.error_dict_full,
                'recaptcha_is_valid': self.request.recaptcha_is_valid,
                'form': self.render_to_string('contacts/popups/estimate_form.html', {
                    'config': config,
                    'form': form_estimate,
                }),
            })