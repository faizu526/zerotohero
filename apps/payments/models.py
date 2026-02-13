from django.db import models
from django.conf import settings

class Payment(models.Model):
    """Payment Records - Stripe & Other Payments"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHODS = [
        ('stripe', 'Stripe Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('wallet', 'Wallet'),
    ]
    
    # User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='payments')
    
    # Order
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, related_name='payments')
    
    # Payment Details
    payment_id = models.CharField(max_length=100, unique=True, help_text='Stripe PaymentIntent ID')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe Data
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_payment_intent = models.CharField(max_length=100, blank=True)
    stripe_payment_method = models.CharField(max_length=100, blank=True)
    
    # Metadata
    description = models.CharField(max_length=200, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment #{self.payment_id} - {self.status}"

