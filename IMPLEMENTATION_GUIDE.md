# 🚀 ZeroToHero Website - Complete Implementation Guide

## Current Status
✅ URL templates fixed and connected
## Table of Contents
1. [Database Models Design and Implementation](#1-database-models-design-and-implementation)
2. [Admin Panel Configuration](#2-admin-panel-configuration)
3. [Search Functionality Implementation](#3-search-functionality-implementation)
4. [Business Logic for Courses/Platforms](#4-business-logic-for-coursesplatforms)
5. [Data Seeding and Testing](#5-data-seeding-and-testing)
6. [Deployment Considerations](#6-deployment-considerations)

## 1. Database Models Design and Implementation

### Core App Models (`apps/core/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
```

### Platforms App Models (`apps/platforms/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Category, Tag

class Platform(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='platforms/', blank=True)
    website = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = (
        ('course', 'Course'),
        ('bundle', 'Bundle'),
        ('resource', 'Resource'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round((1 - self.price / self.original_price) * 100)
        return 0
```

### Learning App Models (`apps/learning/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Category, Tag
from apps.platforms.models import Product

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=100, blank=True)  # e.g., "10 hours"
    instructor = models.CharField(max_length=200, blank=True)
    certificate = models.BooleanField(default=False)
    prerequisites = models.TextField(blank=True)

    def __str__(self):
        return self.product.title

class Roadmap(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='RoadmapCourse')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RoadmapCourse(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('roadmap', 'course')
```

### Users App Models (`apps/users/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_affiliate = models.BooleanField(default=False)
    affiliate_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('platforms.Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.title}"
```

### Cart App Models (`apps/cart/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from apps.platforms.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.cart.user.username} - {self.product.title}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
```

### Orders App Models (`apps/orders/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from apps.platforms.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order

    def __str__(self):
        return f"{self.order.order_number} - {self.product.title}"

    @property
    def total_price(self):
        return self.price * self.quantity
```

### Payments App Models (`apps/payments/models.py`)

```python
from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.order.order_number}"
```

### Affiliate App Models (`apps/affiliate/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User
from apps.platforms.models import Product

class AffiliateLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    affiliate_url = models.URLField()
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.10)  # 10%
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class Commission(models.Model):
    affiliate_link = models.ForeignKey(AffiliateLink, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission for {self.affiliate_link} - {self.amount}"
```

### Implementation Steps for Models

1. Copy the model code above into the respective `models.py` files.
2. Run `python manage.py makemigrations` to create migration files.
3. Run `python manage.py migrate` to apply migrations to the database.

## 2. Admin Panel Configuration

### Core Admin (`apps/core/admin.py`)

```python
from django.contrib import admin
from .models import Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
```

### Platforms Admin (`apps/platforms/admin.py`)

```python
from django.contrib import admin
from .models import Platform, Product

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'product_type', 'price', 'is_active')
    list_filter = ('product_type', 'is_active', 'platform__category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('discount_percentage',)
```

### Learning Admin (`apps/learning/admin.py`)

```python
from django.contrib import admin
from .models import Course, Roadmap, RoadmapCourse

class RoadmapCourseInline(admin.TabularInline):
    model = RoadmapCourse
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('product', 'level', 'duration', 'certificate')
    list_filter = ('level', 'certificate')
    search_fields = ('product__title', 'instructor')

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RoadmapCourseInline]
```

### Users Admin (`apps/users/admin.py`)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Wishlist

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class WishlistInline(admin.TabularInline):
    model = Wishlist
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, WishlistInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'is_affiliate')
    list_filter = ('is_affiliate',)
    search_fields = ('user__username', 'user__email', 'location')
```

### Orders Admin (`apps/orders/admin.py`)

```python
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number',)
    inlines = [OrderItemInline]
```

### Implementation Steps for Admin

1. Copy the admin code into respective `admin.py` files.
2. Access the Django admin at `/admin/` after creating a superuser with `python manage.py createsuperuser`.

## 3. Search Functionality Implementation

### Install Django Haystack and Elasticsearch (Optional but Recommended)

```bash
pip install django-haystack elasticsearch
```

### Configure Haystack in `config/settings.py`

```python
INSTALLED_APPS = [
    # ... existing apps
    'haystack',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'zerotohero',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

### Create Search Indexes

Create `apps/platforms/search_indexes.py`:

```python
from haystack import indexes
from .models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    platform = indexes.CharField(model_attr='platform__name')
    price = indexes.DecimalField(model_attr='price')
    product_type = indexes.CharField(model_attr='product_type')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
```

Create `apps/learning/search_indexes.py`:

```python
from haystack import indexes
from .models import Course

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='product__title')
    description = indexes.CharField(model_attr='product__description')
    level = indexes.CharField(model_attr='level')
    instructor = indexes.CharField(model_attr='instructor')

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(product__is_active=True)
```

### Create Search Templates

Create `templates/search/indexes/platforms/product_text.txt`:

```
{{ object.title }}
{{ object.description }}
{{ object.platform.name }}
{{ object.product_type }}
```

Create `templates/search/indexes/learning/course_text.txt`:

```
{{ object.product.title }}
{{ object.product.description }}
{{ object.level }}
{{ object.instructor }}
```

### Implement Search View

Update `apps/core/views.py`:

```python
from haystack.query import SearchQuerySet
from django.shortcuts import render

def search(request):
    query = request.GET.get('q', '')
    results = SearchQuerySet().filter(content=query) if query else []
    return render(request, 'core/search_results.html', {'query': query, 'results': results})
```

### Implementation Steps for Search

1. Install and configure Elasticsearch.
2. Add Haystack configuration to settings.
3. Create search indexes and templates.
4. Implement search view and template.
5. Run `python manage.py rebuild_index` to build the search index.

## 4. Business Logic for Courses/Platforms

### Platforms Views (`apps/platforms/views.py`)

```python
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Platform, Product
from apps.core.models import Category

def platforms_list(request):
    platforms = Platform.objects.filter(is_active=True)
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        platforms = platforms.filter(category__slug=category_filter)
    paginator = Paginator(platforms, 12)
    page = request.GET.get('page')
    platforms = paginator.get_page(page)
    return render(request, 'platforms/platforms.html', {
        'platforms': platforms,
        'categories': categories,
        'current_category': category_filter
    })

def platform_detail(request, slug):
    platform = get_object_or_404(Platform, slug=slug, is_active=True)
    products = platform.product_set.filter(is_active=True)
    return render(request, 'platforms/platform_detail.html', {
        'platform': platform,
        'products': products
    })

def products_list(request):
    products = Product.objects.filter(is_active=True).select_related('platform')
    category_filter = request.GET.get('category')
    platform_filter = request.GET.get('platform')
    product_type_filter = request.GET.get('type')
    if category_filter:
        products = products.filter(platform__category__slug=category_filter)
    if platform_filter:
        products = products.filter(platform__slug=platform_filter)
    if product_type_filter:
        products = products.filter(product_type=product_type_filter)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'platforms/products.html', {
        'products': products,
        'current_filters': {
            'category': category_filter,
            'platform': platform_filter,
            'type': product_type_filter
        }
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        platform=product.platform, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'platforms/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
```

### Learning Views (`apps/learning/views.py`)

```python
from django.shortcuts import render, get_object_or_404
from .models import Course, Roadmap

def courses_list(request):
    courses = Course.objects.select_related('product').filter(product__is_active=True)
    level_filter = request.GET.get('level')
    if level_filter:
        courses = courses.filter(level=level_filter)
    return render(request, 'learning/courses.html', {
        'courses': courses,
        'current_level': level_filter
    })

def course_detail(request, slug):
    course = get_object_or_404(Course, product__slug=slug, product__is_active=True)
    return render(request, 'learning/course_detail.html', {'course': course})

def roadmaps_list(request):
    roadmaps = Roadmap.objects.filter(is_active=True).prefetch_related('courses__product')
    return render(request, 'learning/roadmaps.html', {'roadmaps': roadmaps})

def roadmap_detail(request, slug):
    roadmap = get_object_or_404(Roadmap, slug=slug, is_active=True)
    roadmap_courses = roadmap.roadmapcourse_set.select_related('course__product').order_by('order')
    return render(request, 'learning/roadmaps_detail.html', {
        'roadmap': roadmap,
        'roadmap_courses': roadmap_courses
    })
```

### Cart Views (`apps/cart/views.py`)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from apps.platforms.models import Product

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.title} added to cart.")
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart:cart_detail')
```

### Orders Views (`apps/orders/views.py`)

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import stripe
from .models import Order, OrderItem
from apps.cart.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            currency=settings.STRIPE_CURRENCY
        )
        # Create order items
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Clear cart
        cart.cartitem_set.all().delete()
        messages.success(request, f"Order {order.order_number} created successfully!")
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
```

## 5. Data Seeding and Testing

### Create Fixtures

Create `fixtures/initial_data.json`:

```json
[
  {
    "model": "core.category",
    "pk": 1,
    "fields": {
      "name": "Programming",
      "slug": "programming",
      "description": "Programming courses and resources"
    }
  },
  {
    "model": "platforms.platform",
    "pk": 1,
    "fields": {
      "name": "Udemy",
      "slug": "udemy",
      "description": "Online learning platform",
      "website": "https://www.udemy.com",
      "category": 1,
      "is_active": true
    }
  }
]
```

### Load Fixtures

```bash
python manage.py loaddata fixtures/initial_data.json
```

### Create Management Command for Data Seeding

Create `apps/core/management/commands/seed_data.py`:

```python
from django.core.management.base import BaseCommand
from apps.core.models import Category
from apps.platforms.models import Platform, Product

class Command(BaseCommand):
    help = 'Seed initial data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Programming', 'slug': 'programming'},
            {'name': 'Design', 'slug': 'design'},
            {'name': 'Business', 'slug': 'business'},
        ]
        for cat_data in categories_data:
            Category.objects.get_or_create(**cat_data)

        # Create platforms
        platforms_data = [
            {'name': 'Udemy', 'slug': 'udemy', 'website': 'https://udemy.com', 'category_id': 1},
            {'name': 'Coursera', 'slug': 'coursera', 'website': 'https://coursera.org', 'category_id': 1},
        ]
        for plat_data in platforms_data:
            Platform.objects.get_or_create(**plat_data)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully'))
```

### Run Seeding Command

```bash
python manage.py seed_data
```

### Testing

Create tests in `apps/platforms/tests.py`:

```python
from django.test import TestCase
from .models import Platform, Product
from apps.core.models import Category

class PlatformModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.platform = Platform.objects.create(
            name='Test Platform',
            slug='test-platform',
            description='Test description',
            website='https://test.com',
            category=self.category
        )

    def test_platform_creation(self):
        self.assertEqual(self.platform.name, 'Test Platform')
        self.assertEqual(self.platform.slug, 'test-platform')
        self.assertTrue(self.platform.is_active)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.platform = Platform.objects.create(
            name='Test Platform',
            slug='test-platform',
            description='Test description',
            website='https://test.com',
            category=self.category
        )
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='Test product description',
            platform=self.platform,
            product_type='course',
            price=99.99
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.discount_percentage, 0)

    def test_discount_percentage(self):
        self.product.original_price = 199.99
        self.product.save()
        self.assertEqual(self.product.discount_percentage, 50)
```

### Run Tests

```bash
python manage.py test
```

## 6. Deployment Considerations

### Environment Variables

Create `.env` file for production:

```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/zerotohero
REDIS_URL=redis://localhost:6379
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Production Settings

Update `config/settings.py` for production:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Static files for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Docker Configuration

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=zerotohero
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
  static:
```

### Deployment Steps

1. Set up production database (PostgreSQL recommended).
2. Configure web server (Nginx + Gunicorn).
3. Set up SSL certificate (Let's Encrypt).
4. Configure backup strategy.
5. Set up monitoring and logging.
6. Deploy using Docker or cloud platform (Heroku, AWS, etc.).

### Performance Optimization

1. Use database indexing on frequently queried fields.
2. Implement caching with Redis.
3. Optimize images and static files.
4. Use CDN for static assets.
5. Implement pagination for large datasets.
6. Use select_related and prefetch_related in queries.

This comprehensive guide covers all the essential components to make your ZeroToHero e-commerce platform fully functional. Follow the steps in order, and you'll have a robust, scalable platform ready for production.
