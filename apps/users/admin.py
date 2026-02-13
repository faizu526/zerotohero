from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, UserSettings, Enrollment, UserProgress, Wishlist, Certificate

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'wallet_balance', 'is_active']
    list_filter = ['user_type', 'is_active', 'email_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Zero To Hero Info', {
            'fields': ['user_type', 'phone', 'avatar', 'wallet_balance', 'total_earned', 'affiliate_code', 'email_verified']
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'company', 'city', 'country']
    search_fields = ['user__username', 'occupation', 'company']

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 'email_course_updates']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'progress', 'status', 'enrolled_at']
    list_filter = ['status']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'certificate_id', 'issued_at']
