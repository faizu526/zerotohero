from django.urls import path
from . import views

urlpatterns = [
    path('hidden-gems/', views.hidden_gems, name='hidden-gems'),
    path('hidden-gems/<slug:slug>/', views.hidden_gem_detail, name='hidden-gem-detail'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('roadmap/<slug:slug>/', views.roadmap_single, name='roadmap-single'),
    path('certifications/', views.certifications, name='certifications'),
    path('labs/', views.labs, name='labs'),
]

