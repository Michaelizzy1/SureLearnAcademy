from django.conf import settings

from .seo import absolute


def seo(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "WHATSAPP_URL": settings.WHATSAPP_URL,
        "SOCIAL_INSTAGRAM": settings.SOCIAL_INSTAGRAM,
        "SOCIAL_FACEBOOK": settings.SOCIAL_FACEBOOK,
        "SOCIAL_X": settings.SOCIAL_X,
        "CANONICAL_URL": absolute(request.path),
        "DEFAULT_OG_IMAGE": absolute("/static/assets/og-default.png"),
    }
