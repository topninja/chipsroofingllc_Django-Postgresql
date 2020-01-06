from ipware.ip import get_ip
from django.views.generic.base import View
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from libs.cookies import set_cookie
from libs.views_ajax import AjaxViewMixin
from .models import RatingVote
from . import conf


class VoteView(AjaxViewMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        rating = request.POST.get('rating', 5)
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            rating = 5

        # проверка, что уже голосовал (по куке)
        last_rating = request.COOKIES.get('voted')
        is_voted = last_rating is not None

        # проверка, что уже голосовал (по IP)
        client_ip = get_ip(request)
        last_vote = RatingVote.objects.filter(
            ip=client_ip,
            date__gte=now() - timedelta(seconds=conf.REVOTE_PERIOD)
        ).first()
        if last_vote:
            last_rating = last_vote.rating
            is_voted = True

        if is_voted:
            response = self.json_response({
                'error': _('Already voted!'),
                'rating': last_rating,
            })
            set_cookie(response, 'voted', last_rating, expires=conf.COOKIE_DAYS_EXPIRES)
            return response

        # голосование
        vote = RatingVote(
            ip=client_ip,
            rating=rating,
        )
        try:
            vote.full_clean()
            vote.save()
        except ValidationError:
            return self.json_error()
        else:
            response = self.json_response({
                'rating': rating,
            })
            set_cookie(response, 'voted', rating, expires=conf.COOKIE_DAYS_EXPIRES)
            return response
