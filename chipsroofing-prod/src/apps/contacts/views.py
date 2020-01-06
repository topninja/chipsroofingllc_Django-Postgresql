from django.template import loader
from django.utils.html import escape
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from seo.seo import Seo
from libs.email import send_template
from libs.views import CachedViewMixin
from .models import ContactsConfig, Address, NotificationReceiver
from .forms import ContactForm


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'contacts/index.html'
    config = None
    address = None

    def last_modified(self, *args, **kwargs):
        self.config = ContactsConfig.get_solo()
        self.address = Address.objects.get()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        form = ContactForm()

        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header,
        })
        seo.save(request)

        request.breadcrumbs.add('CONTACT')

        return self.render_to_response({
            'config': self.config,
            'address': self.address,
            'page_data': self.config,
            'is_contact_page': True,
            'form': form,
        })
    #
    # def post(self, request):
    #     config = ContactsConfig.get_solo()
    #     form = ContactForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         message = form.save(commit=False)
    #         referer = request.POST.get('referer', request.build_absolute_uri(request.path_info))
    #         message.referer = escape(referer)
    #         message.save()
    #
    #         receivers = NotificationReceiver.objects.all().values_list('email', flat=True)
    #         send_template(request, receivers,
    #                       subject=_('Message from {domain}'),
    #                       template='contacts/mails/message.html',
    #                       context={
    #                           'message': message,
    #                       }
    #                       )
    #
    #         return redirect('contacts:index')
    #     else:
    #         return self.render_to_response({
    #             'config': config,
    #             'address': self.address,
    #             'form': form,
    #         })


def contact_block_render(context, block, **kwargs):
    """ Рендеринг подключаемого блока контактов """
    return loader.render_to_string('contacts/block.html', {
        'config': ContactsConfig.get_solo(),
        'address': Address.objects.get(),
        'block': block,
    }, request=context.get('request'))
