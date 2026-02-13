"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from apps.core.views import HomeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', RedirectView.as_view(pattern_name='dashboard-overview', permanent=False)),
    path('core/', include('apps.core.urls')),
    path('platforms/', include('apps.platforms.urls')),
    path('learning/', include('apps.learning.urls')),
    path('affiliate/', include('apps.affiliate.urls')),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.core.authurls')),
    path('cart/', include('apps.cart.urls')),
    path('payments/', include('apps.payments.urls')),
    path('analytics/', include('apps.core.analytics_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
