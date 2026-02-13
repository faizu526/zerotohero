from django.contrib import admin
from .models import PlatformCategory, Platform, ProductCategory, Product, Bundle

@admin.register(PlatformCategory)
class PlatformCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'category', 'commission_rate', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'difficulty']
    search_fields = ['name', 'country', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'category', 'original_price', 'our_price', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'difficulty', 'product_type']
    search_fields = ['name', 'description', 'platform__name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'bundle_price', 'savings_percentage', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['products']
