# apps/core/context_processors.py

from django.conf import settings


def google_analytics(request):
    """Add Google Analytics tracking ID to template context"""
    return {
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
    }


def site_settings(request):
    """Add site-wide settings to template context"""
    return {
        'SITE_NAME': 'Zero To Hero',
        'SITE_URL': request.build_absolute_uri('/'),
    }
