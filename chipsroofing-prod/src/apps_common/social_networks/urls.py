import inspect
from django.conf.urls import url
from . import conf
from . import rss

urlpatterns = []

for name, member in inspect.getmembers(rss, predicate=inspect.isclass):
    if issubclass(member, rss.SocialRssFeed) and member.network in conf.ALLOWED_NETWORK_NAMES:
        urlpatterns.append(
            url(r'^rss/{}/$'.format(member.network), member(), name=member.network)
        )
