from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('process/', views.process_payment, name='process-payment'),
    path('success/', views.payment_success, name='payment-success'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    
    # Razorpay Payment URLs
    path('razorpay/checkout/', views.razorpay_checkout, name='razorpay-checkout'),
    path('razorpay/verify/', views.razorpay_payment_verify, name='razorpay-verify'),
    path('razorpay/webhook/', views.razorpay_webhook, name='razorpay-webhook'),
]
