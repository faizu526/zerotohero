from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/overview/', views.dashboard_overview, name='dashboard-overview'),
    path('dashboard/my-courses/', views.dashboard_my_courses, name='dashboard-my-courses'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard-orders'),
    path('dashboard/wishlist/', views.dashboard_wishlist, name='dashboard-wishlist'),
    path('dashboard/settings/', views.dashboard_settings, name='dashboard-settings'),
    path('dashboard/affiliate/', views.dashboard_affiliate, name='dashboard-affiliate'),
]