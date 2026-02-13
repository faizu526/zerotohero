from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Founder, Mission, ImpactStat, 
    ContactMessage, FAQCategory, FAQ, BlogCategory, BlogPost
)

# ===== SITE SETTINGS ADMIN =====
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'hero_title', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'hero_title', 'hero_subtitle', 'hero_description')
        }),
        ('Stats Counters', {
            'fields': ('platforms_count', 'hidden_gems_count', 'countries_count', 'students_count')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Logo & Favicon', {
            'fields': ('logo', 'favicon'),
            'classes': ('collapse',)
        }),
    )

# ===== FOUNDER ADMIN =====
@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'years_of_experience', 'is_active']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'title', 'bio', 'story', 'avatar')
        }),
        ('Social Links', {
            'fields': ('twitter', 'github', 'linkedin', 'email'),
            'classes': ('collapse',)
        }),
        ('Stats', {
            'fields': ('years_of_experience', 'certifications', 'students_mentored'),
            'classes': ('collapse',)
        }),
    )

# ===== MISSION ADMIN =====
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order']
    list_editable = ['order']

# ===== IMPACT STAT ADMIN =====
@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'prefix', 'suffix', 'order']
    list_editable = ['order']

# ===== CONTACT MESSAGE ADMIN =====
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at', 'ip_address']
    list_editable = ['status']

# ===== FAQ CATEGORY ADMIN =====
@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    list_editable = ['order']

# ===== FAQ ADMIN =====
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']

# ===== BLOG CATEGORY ADMIN =====
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# ===== BLOG POST ADMIN =====
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 'views', 'published_at']
    list_filter = ['status', 'is_featured', 'is_hidden_gem', 'category', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at', 'published_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'author', 'featured_image', 'excerpt', 'content')
        }),
        ('Metadata', {
            'fields': ('read_time', 'is_featured', 'is_hidden_gem', 'status', 'views')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Admin Site Customization
admin.site.site_header = '🚀 Zero To Hero Admin'
admin.site.site_title = 'Zero To Hero'
admin.site.index_title = 'Dashboard Overview'

