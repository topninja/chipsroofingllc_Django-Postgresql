from django.shortcuts import resolve_url
from django.utils.html import strip_tags
from django.contrib.syndication.views import Feed
from .models import FeedPost
from . import conf


class SocialRssFeed(Feed):
    title = ''
    description = ''
    network = None
    items_count = 20

    def __init__(self):
        if self.network not in dict(conf.ALL_NETWORKS):
            raise ValueError("unknown feed network: '%s'" % self.network)

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def link(self):
        return resolve_url('social_networks:%s' % self.network)

    def items(self):
        qs = FeedPost.objects.filter(for_network=self.network)
        return qs[:self.items_count]

    def item_link(self, item):
        """ URL элемента """
        return item.url

    def item_title(self, item):
        """ Заголовок элемента """
        return strip_tags(item.text)

    def item_description(self, item):
        """ Описание элемента """
        return None

    def item_pubdate(self, item):
        """ Дата публикации """
        return item.created

    def item_guid(self, item):
        """ Уникальный идентификатор (обязательно ID поста) """
        return str(item.id)


class GoogleFeed(SocialRssFeed):
    title = 'Google Plus feed'
    description = 'Google Plus feed'
    network = conf.NETWORK_GOOGLE


class FacebookFeed(SocialRssFeed):
    title = 'Facebook feed'
    description = 'Facebook feed'
    network = conf.NETWORK_FACEBOOK


class TwitterFeed(SocialRssFeed):
    title = 'Twitter feed'
    description = 'Twitter feed'
    network = conf.NETWORK_TWITTER


class LinkedInFeed(SocialRssFeed):
    title = 'LinkedIn feed'
    description = 'LinkedIn feed'
    network = conf.NETWORK_LINKEDIN
