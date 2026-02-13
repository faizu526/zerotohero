"""
Analytics URLs for Zero To Hero
"""
from django.urls import path
from . import analytics_views

urlpatterns = [
    path('', analytics_views.analytics_dashboard, name='analytics-dashboard'),
    path('users/', analytics_views.user_analytics, name='user-analytics'),
    path('sales/', analytics_views.sales_analytics, name='sales-analytics'),
    path('affiliates/', analytics_views.affiliate_analytics, name='affiliate-analytics'),
]
