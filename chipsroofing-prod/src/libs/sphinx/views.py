from django.views.generic import View
from django.http.response import StreamingHttpResponse, Http404
from .index import ALL_INDEXES, SphinxXMLIndex
from . import conf


class IndexPipeView(View):
    """ Вьюха, отдающая сфинксу XML индекса """
    def get(self, request, index_name, secret):
        if request.method.lower() == 'head':
            raise Http404

        if secret != conf.SECRET:
            raise Http404

        if index_name not in ALL_INDEXES:
            raise Http404

        cls = ALL_INDEXES[index_name]
        if not issubclass(cls, SphinxXMLIndex):
            raise Http404

        index = cls()
        return StreamingHttpResponse(iter(index), content_type='application/xml')
