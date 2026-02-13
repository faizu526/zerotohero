# apps/platforms/models.py
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from decimal import Decimal

class PlatformCategory(models.Model):
    """Platform Categories - Cybersecurity, Programming, etc"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Platform Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Platform(models.Model):
    """500+ Global Learning Platforms"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    ]
    
    COMMISSION_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='platforms/', blank=True)
    website = models.URLField()
    
    # Location
    country = models.CharField(max_length=100, blank=True, default='Global')
    flag = models.CharField(max_length=10, blank=True, help_text='🇮🇳 🇺🇸 🇬🇧 etc')
    
    # Categorization
    category = models.ForeignKey(PlatformCategory, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    description = RichTextField()
    
    # ===== 3:3:3:3 COMMISSION SETTINGS =====
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPE_CHOICES, default='percentage')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)
    our_margin = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)
    student_price_markup = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Affiliate Settings
    affiliate_link = models.URLField(blank=True)
    affiliate_code = models.CharField(max_length=100, blank=True)
    cookie_duration = models.IntegerField(default=30, help_text='Days')
    
    # Features
    is_hidden_gem = models.BooleanField(default=False, help_text='💎 90% students don\'t know')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Statistics (Auto-updated)
    total_products = models.IntegerField(default=0, editable=False)
    total_students = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'name']
    
    def __str__(self):
        return f"{self.flag} {self.name}"
    
    @property
    def display_commission(self):
        if self.commission_type == 'percentage':
            return f"{self.commission_rate}%"
        return f"₹{self.commission_rate}"
    
    def update_product_count(self):
        self.total_products = self.products.count()
        self.save()


class ProductCategory(models.Model):
    """Product Categories - Courses, Labs, Certifications"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """1000+ Courses & Subscriptions"""
    
    PRODUCT_TYPES = [
        ('course', 'Course'),
        ('subscription', 'Subscription'),
        ('lab', 'Lab'),
        ('certification', 'Certification'),
        ('bundle', 'Bundle'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    ]
    
    # Relationships
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    
    # Basic Info
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Media
    image = models.ImageField(upload_to='products/', blank=True)
    preview_video = models.URLField(blank=True)
    
    # ===== 94% PRICING MODEL =====
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    our_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='INR')
    
    # Commission
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=3.00)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    # Details
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.IntegerField(null=True, blank=True)
    has_certificate = models.BooleanField(default=False)
    
    # Links
    affiliate_link = models.URLField(blank=True)
    purchase_link = models.URLField(blank=True)
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Statistics
    students_enrolled = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.platform.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate commission amount
        self.commission_amount = (self.original_price * self.commission_rate) / 100
        super().save(*args, **kwargs)
        
        # Update platform product count
        self.platform.update_product_count()
    
    @property
    def savings_amount(self):
        """Student savings vs market price"""
        return self.original_price - self.our_price
    
    @property
    def savings_percentage(self):
        """Savings percentage"""
        if self.original_price:
            return round(((self.original_price - self.our_price) / self.original_price) * 100, 1)
        return 0


class Bundle(models.Model):
    """Course Bundles - Multiple products together"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    image = models.ImageField(upload_to='bundles/', blank=True)
    
    # Products in bundle
    products = models.ManyToManyField(Product, related_name='bundles')
    
    # Pricing
    original_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2)
    savings_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    savings_percentage = models.IntegerField(editable=False)
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def calculate_totals(self):
        """Calculate original total and savings"""
        total = sum(product.our_price for product in self.products.all())
        self.original_total = total
        self.savings_amount = total - self.bundle_price
        if total:
            self.savings_percentage = int((self.savings_amount / total) * 100)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.calculate_totals()
        super().save(*args, **kwargs)