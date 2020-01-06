from django.conf import settings


def google_recaptcha_public_key(request):
    return {
        'GOOGLE_RECAPTCHA_PUBLIC_KEY': settings.GOOGLE_RECAPTCHA_PUBLIC_KEY,
    }