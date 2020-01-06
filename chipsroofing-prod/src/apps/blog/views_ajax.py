from django.http.response import Http404
from paginator.paginator import Paginator
from django.views.generic.base import View
from django.core.paginator import EmptyPage
from libs.views_ajax import AjaxViewMixin
from .models import BlogPost


class BlogView(AjaxViewMixin, View):
    def get(self, request):
        perpage = request.GET.get('perpage', '')
        params = {}

        try:
            paginator = Paginator(
                request,
                object_list=BlogPost.objects.filter(visible=True),
                per_page=perpage,
                page_neighbors=1,
                side_neighbors=1,
                allow_empty_first_page=False,
            )
        except EmptyPage:
            raise Http404

        params.update({'paginator': paginator, })

        return self.json_response({
            'success_message': self.render_to_string('blog/articles.html', params, ),
        })
