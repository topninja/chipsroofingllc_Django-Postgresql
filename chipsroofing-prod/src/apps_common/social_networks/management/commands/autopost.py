import twitter
import logging
import facebook
from PyLinkedinAPI.PyLinkedinAPI import PyLinkedinAPIClientError
from django.utils.timezone import now
from django.core.management import BaseCommand
from ...models import FeedPost
from ... import conf
from ... import api

MAX_POSTS_PER_CALL = 3
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'
    facebook_api = None
    linkedin_api = None

    def autopost_twitter(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_TWITTER)[:MAX_POSTS_PER_CALL]
        for post in posts:
            try:
                api.twitter.post(post.text, url=post.url)
            except twitter.TwitterError as e:
                logger.error("Twitter Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Twitter Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def autopost_facebook(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_FACEBOOK)[:MAX_POSTS_PER_CALL]
        for post in posts:
            try:
                api.facebook.post(post.text, url=post.url)
            except facebook.GraphAPIError as e:
                logger.error("Facebook Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Facebook Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def autopost_linkedin(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_LINKEDIN)[:MAX_POSTS_PER_CALL]
        for post in posts:
            try:
                api.linkedin.post(post.text, url=post.url)
            except PyLinkedinAPIClientError as e:
                logger.error("Linkedin Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Linkedin Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def handle(self, *args, **options):
        # === Twitter ===
        self.autopost_twitter()

        # === Facebook ===
        self.autopost_facebook()

        # === LinkedIn ===
        self.autopost_linkedin()
