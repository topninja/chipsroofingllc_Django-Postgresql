from django.http.response import Http404
from django.views.generic.base import View
from paginator.paginator import Paginator
from libs.views_ajax import AjaxViewMixin
from .models import ExamplesPageConfig
from django.core.paginator import EmptyPage


class ExamplesView(AjaxViewMixin, View):
    def get(self, request):
        perpage = request.GET.get('perpage', '')
        params = {}
        self.config = ExamplesPageConfig.get_solo()

        try:
            paginator = Paginator(
                request,
                object_list=self.config.gallery.image_items,
                per_page=perpage,
                page_neighbors=1,
                side_neighbors=1,
                allow_empty_first_page=False,
            )
        except EmptyPage:
            raise Http404

        params.update({'paginator': paginator, })

        return self.json_response({
            'success_message': self.render_to_string('examples/items.html', params, ),
        })
