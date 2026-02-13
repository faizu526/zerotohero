from django.urls import path
from . import views

urlpatterns = [
    # Products List
    path('', views.ProductListView.as_view(), name='products'),
    
    # Product Detail
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]