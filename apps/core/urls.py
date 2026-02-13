# apps/core/urls.py - COPY PASTE KARO
from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.HomeView.as_view(), name='home'),
    
    # About Page
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Contact Page
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # FAQ Page
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    # Blog Pages
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
