# apps/learning/models.py
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class GemCategory(models.Model):
    """Hidden Gems Categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text='🇮🇳 🇺🇳 etc')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Gem Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class HiddenGem(models.Model):
    """💎 200+ Secret Resources - 90% Students Don't Know"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(GemCategory, on_delete=models.CASCADE, related_name='gems')
    
    # Provider Info
    provider = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    flag = models.CharField(max_length=10, help_text='🇮🇳 🇺🇳 🇺🇸 etc')
    
    # Details
    description = models.TextField()
    why_hidden = models.TextField(help_text='Why 90% students miss this')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Resource Info
    url = models.URLField()
    has_certificate = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    language = models.CharField(max_length=100, default='English')
    
    # Features
    icon = models.CharField(max_length=50, blank=True, help_text='Emoji or icon class')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Statistics
    views = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'name']
    
    def __str__(self):
        return f"{self.flag} {self.name}"


class Roadmap(models.Model):
    """Learning Roadmaps - Career Paths"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='🛣️')
    
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_months = models.IntegerField(default=6)
    
    # Statistics
    total_phases = models.IntegerField(default=0, editable=False)
    total_resources = models.IntegerField(default=0, editable=False)
    hidden_gems_count = models.IntegerField(default=0)
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'title']
    
    def __str__(self):
        return self.title
    
    def update_stats(self):
        self.total_phases = self.phases.count()
        self.save()


class RoadmapPhase(models.Model):
    """Individual Phase in a Roadmap"""
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='phases')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    month_start = models.IntegerField(help_text='Starting month')
    month_end = models.IntegerField(help_text='Ending month')
    
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.roadmap.title} - {self.title}"


class Certification(models.Model):
    """Free + Paid Certifications"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    PRICE_TYPE_CHOICES = [
        ('free', 'Free'),
        ('free_with_aid', 'Free with Financial Aid'),
        ('paid', 'Paid'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    # Provider
    provider = models.CharField(max_length=100)
    provider_logo = models.ImageField(upload_to='certifications/', blank=True)
    
    # Details
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_hours = models.IntegerField(null=True, blank=True)
    
    # Pricing
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    our_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Links
    official_url = models.URLField()
    affiliate_link = models.URLField(blank=True)
    
    # Features
    is_hidden_gem = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.provider} - {self.name}"


class Lab(models.Model):
    """Hands-on Practice Environments"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    # Provider
    provider = models.CharField(max_length=100)
    provider_logo = models.ImageField(upload_to='labs/', blank=True)
    
    # Details
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    lab_count = models.IntegerField(default=1, help_text='Number of labs/challenges')
    
    # Pricing
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    our_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Links
    url = models.URLField()
    
    # Features
    is_hidden_gem = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name