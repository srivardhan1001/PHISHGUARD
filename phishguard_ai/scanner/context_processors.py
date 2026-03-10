from django.conf import settings


def api_config(request):
    enabled = getattr(settings, "ENABLE_EXTERNAL_API", True)
    has_key = bool(getattr(settings, "GOOGLE_SAFEBROWSING_API_KEY", None))
    return {
        "api_enabled": enabled,
        "api_has_key": has_key,
    }

