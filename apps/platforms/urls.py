from django.urls import path
from . import views

urlpatterns = [
    # Platforms List
    path('', views.PlatformListView.as_view(), name='platforms'),
    
    # Products (MUST come before slug patterns)
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Bundles (MUST come before slug patterns)
    path('bundles/', views.BundleListView.as_view(), name='bundles'),
    
    # Platform Detail (by id - for backwards compatibility)
    path('platform/<int:id>/', views.platform_detail_by_id, name='platform-single'),
    
    # Platform Detail (by slug - MUST be last)
    path('<slug:slug>/', views.PlatformDetailView.as_view(), name='platform_detail'),
]
