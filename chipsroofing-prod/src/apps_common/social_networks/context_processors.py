from .models import SocialConfig


def google_apikey(request):
    config = SocialConfig.get_solo()
    return {
        'GOOGLE_APIKEY': config.google_apikey,
    }
