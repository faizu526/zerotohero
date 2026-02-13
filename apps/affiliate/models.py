# apps/affiliate/models.py
from django.db import models
from django.conf import settings
from decimal import Decimal

class PricingPlan(models.Model):
    """Student Pricing Plans"""
    
    BILLING_CYCLES = [
        ('free', 'Free'),
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='💰')
    
    # Pricing
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='INR')
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # Commission
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    @property
    def savings_amount(self):
        if self.compare_at_price:
            return self.compare_at_price - self.price
        return 0


class PlanFeature(models.Model):
    """Features for each pricing plan"""
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.plan.name} - {self.feature}"


class Affiliate(models.Model):
    """Affiliate Program - 3:3:3:3 Model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='affiliate_profile')
    
    # Affiliate Code
    referral_code = models.CharField(max_length=50, unique=True)
    referral_link = models.URLField(blank=True)
    
    # Earnings
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Statistics
    total_clicks = models.IntegerField(default=0)
    total_conversions = models.IntegerField(default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Payment Details
    PAYMENT_METHODS = [
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
        ('wallet', 'Wallet'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='upi')
    payment_details = models.JSONField(default=dict)
    
    # Status
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.referral_code}"
    
    def generate_referral_link(self):
        base_url = settings.BASE_URL or 'https://zerotohero.tech'
        self.referral_link = f"{base_url}/ref/{self.referral_code}/"
        self.save()


class Commission(models.Model):
    """Commission earned from sales"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='commissions')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True)
    
    # Commission Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    platform = models.ForeignKey('platforms.Platform', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('platforms.Product', on_delete=models.SET_NULL, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.affiliate.user.username} - ₹{self.amount}"


class Withdrawal(models.Model):
    """Affiliate withdrawal requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment
    payment_method = models.CharField(max_length=20)
    payment_details = models.JSONField()
    transaction_id = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.affiliate.user.username} - ₹{self.amount} - {self.status}"