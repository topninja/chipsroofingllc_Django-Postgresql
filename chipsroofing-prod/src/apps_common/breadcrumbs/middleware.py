from .breadcrumbs import Breadcrumbs


class BreadcrumbsMiddleware:
    @staticmethod
    def process_request(request):
        request.breadcrumbs = Breadcrumbs()
