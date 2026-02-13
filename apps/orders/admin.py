from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total', 'payment_status', 'order_status', 'created_at']
    list_filter = ['payment_status', 'order_status']
    search_fields = ['order_number', 'user__username', 'guest_email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'platform_name', 'price', 'commission_amount']
