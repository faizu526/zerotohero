# apps/core/models.py
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class SiteSettings(models.Model):
    """Home Page Settings - Hero, Stats, SEO"""
    site_name = models.CharField(max_length=100, default='Zero To Hero')
    hero_title = models.CharField(max_length=200, default='Zero To Hero')
    hero_subtitle = models.CharField(max_length=200, default='Your Journey Starts Here')
    hero_description = models.TextField(blank=True)
    
    # Stats Counters (500+, 200+, etc)
    platforms_count = models.IntegerField(default=500)
    hidden_gems_count = models.IntegerField(default=200)
    countries_count = models.IntegerField(default=50)
    students_count = models.IntegerField(default=50000)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Logo & Favicon
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.site_name


class Founder(models.Model):
    """About Page - Founder Information"""
    name = models.CharField(max_length=100, default='Faizu')
    title = models.CharField(max_length=200, default='Cybersecurity Student · Ethical Hacker · Developer')
    bio = models.TextField()
    story = models.TextField(help_text='Zero to Hero journey')
    avatar = models.ImageField(upload_to='founder/', blank=True)
    
    # Social Links
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    email = models.EmailField(default='faizu@zerotohero.tech')
    
    # Stats
    years_of_experience = models.IntegerField(default=4)
    certifications = models.IntegerField(default=5)
    students_mentored = models.IntegerField(default=5000)
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Founder'
        verbose_name_plural = 'Founder'
    
    def __str__(self):
        return self.name


class Mission(models.Model):
    """About Page - Mission & Values"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text='Emoji or icon class')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class ImpactStat(models.Model):
    """About Page - Impact Numbers"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)  # 50K+, ₹2.5Cr+, etc
    prefix = models.CharField(max_length=10, blank=True, help_text='₹, +, etc')
    suffix = models.CharField(max_length=10, blank=True, help_text='K+, Cr+, etc')
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactMessage(models.Model):
    """Contact Page - Form Submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('spam', 'Spam'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject[:50]}"


class FAQCategory(models.Model):
    """FAQ Page - Categories"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    """FAQ Page - Questions & Answers"""
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question[:100]


class BlogCategory(models.Model):
    """Blog Page - Categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog Page - Articles"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=100, default='Faizu')
    
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    excerpt = models.TextField(max_length=300, help_text='Short summary')
    content = RichTextField()
    
    # Metadata
    read_time = models.IntegerField(default=5, help_text='Minutes')
    is_featured = models.BooleanField(default=False)
    is_hidden_gem = models.BooleanField(default=False, help_text='💎 Hidden Gem related')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
