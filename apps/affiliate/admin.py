from django.contrib import admin
from .models import PricingPlan, PlanFeature, Affiliate, Commission, Withdrawal

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'billing_cycle', 'price', 'is_featured', 'is_active']
    list_filter = ['billing_cycle', 'is_featured', 'is_active']

@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ['plan', 'feature', 'is_included']

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'total_earned', 'available_balance', 'is_active']
    list_filter = ['is_active', 'payment_method']

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['affiliate', 'amount', 'rate', 'status', 'created_at']
    list_filter = ['status']

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['affiliate', 'amount', 'status', 'requested_at']
    list_filter = ['status']
