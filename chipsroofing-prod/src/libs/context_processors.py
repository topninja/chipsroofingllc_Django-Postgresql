from django.contrib.sites.shortcuts import get_current_site


def domain(request):
    site = get_current_site(request)
    return {
        'domain': site.domain,
    }
