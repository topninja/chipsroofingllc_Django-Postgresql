import re
from django.contrib.sites.shortcuts import get_current_site


class SubdomainMiddleware:
    @staticmethod
    def process_request(request):
        domain = request.get_host().lower()
        site_domain = get_current_site(request).domain.lower()

        re_subdomains = '^(.*)\.%s$' % site_domain.replace('.', '\.')
        match = re.match(re_subdomains, domain, re.IGNORECASE)
        if match is None:
            return

        request.subdomain = match.group(1)
