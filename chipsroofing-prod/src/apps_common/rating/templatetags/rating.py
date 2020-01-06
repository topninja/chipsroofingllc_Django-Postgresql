from django.db import models
from django.template import Library, loader
from django.db.models.functions import Coalesce
from libs.cache.cached import cached
from ..models import RatingVote

register = Library()


@cached(time=10*60)
def get_rating():
    return {
        'count': RatingVote.objects.count(),
        'avg': RatingVote.objects.aggregate(rating=Coalesce(models.Avg('rating'), 0))['rating']
    }


@register.simple_tag(takes_context=True)
def rating(context):
    return loader.render_to_string('rating/voting.html', {
        'rating': get_rating(),
    }, request=context.get('request'))
