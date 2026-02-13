from django.db import models
from django.conf import settings

class CartItem(models.Model):
    """Shopping Cart Items - Database backed cart"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    # Product
    product = models.ForeignKey('platforms.Product', on_delete=models.CASCADE, related_name='cart_items')
    
    # Quantity
    quantity = models.IntegerField(default=1)
    
    # Price snapshot
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'product', 'session_key']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user or self.session_key} - {self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity

