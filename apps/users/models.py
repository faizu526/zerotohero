# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    """Custom User Model - Zero To Hero"""
    
    USER_TYPE_CHOICES = [
        ('student', '🎓 Student'),
        ('affiliate', '🤝 Affiliate'),
        ('admin', '👨‍💼 Admin'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Wallet & Earnings
    wallet_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Affiliate
    affiliate_code = models.CharField(max_length=50, unique=True, blank=True)
    affiliate_referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )
    
    # Verification
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"
    
    def save(self, *args, **kwargs):
        if not self.affiliate_code:
            self.affiliate_code = self.generate_affiliate_code()
        super().save(*args, **kwargs)
    
    def generate_affiliate_code(self):
        while True:
            code = get_random_string(8).upper()
            if not User.objects.filter(affiliate_code=code).exists():
                return code
    
    @property
    def profile_completion(self):
        score = 0
        total = 5
        if self.first_name: score += 1
        if self.last_name: score += 1
        if self.email_verified: score += 1
        if self.phone: score += 1
        if self.avatar: score += 1
        return int((score / total) * 100)


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    # Social
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class UserSettings(models.Model):
    """Dashboard Settings Page"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    
    # Display
    theme = models.CharField(max_length=20, default='light')
    language = models.CharField(max_length=10, default='en')
    
    # Notifications
    email_course_updates = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=False)
    email_affiliate = models.BooleanField(default=True)
    
    # Privacy
    profile_public = models.BooleanField(default=True)
    show_wishlist = models.BooleanField(default=True)
    show_certificates = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Settings - {self.user.username}"


class Enrollment(models.Model):
    """My Courses - Student Enrollments"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    product = models.ForeignKey('platforms.Product', on_delete=models.CASCADE)
    
    # Progress
    progress = models.IntegerField(default=0, help_text='Percentage 0-100')
    last_accessed = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Access
    enrolled_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.progress}%"


class UserProgress(models.Model):
    """Dashboard - Detailed progress tracking"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress_items')
    module_name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['enrollment', 'module_name']


class Wishlist(models.Model):
    """Wishlist - Saved Courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('platforms.Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Certificate(models.Model):
    """User Certificates"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    product = models.ForeignKey('platforms.Product', on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=100, unique=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True)

    issued_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class UserSkillProgress(models.Model):
    """Skill Progress System - Track user skills and progress"""
    
    DEFAULT_SKILLS = [
        'Python',
        'Networking',
        'Cybersecurity',
        'Web Security',
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_progress')
    skill_name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    progress_percent = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    is_unlocked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'skill_name']
        ordering = ['skill_name']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill_name} (Level {self.level})"
    
    @classmethod
    def create_default_skills(cls, user):
        """Create default skills for a user if they don't exist"""
        created_skills = []
        for skill_name in cls.DEFAULT_SKILLS:
            skill, created = cls.objects.get_or_create(
                user=user,
                skill_name=skill_name,
                defaults={
                    'level': 1,
                    'progress_percent': 0,
                    'xp': 0,
                    'is_unlocked': True,
                }
            )
            if created:
                created_skills.append(skill)
        return created_skills


class EmailOTP(models.Model):
    """Email OTP Verification System"""
    OTP_TYPE_CHOICES = [
        ('signup', 'Signup Verification'),
        ('password_reset', 'Password Reset'),
        ('email_change', 'Email Change'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_otps', null=True, blank=True)
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES, default='signup')
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Expiry
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    # Attempts tracking
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email OTP'
        verbose_name_plural = 'Email OTPs'
    
    def __str__(self):
        return f"{self.email} - {self.otp_type} - {'Verified' if self.is_verified else 'Pending'}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def can_attempt(self):
        return self.attempts < self.max_attempts and not self.is_verified and not self.is_expired()
    
    def verify(self, code):
        """Verify OTP code"""
        from django.utils import timezone
        
        if not self.can_attempt():
            return False, "OTP expired or max attempts reached"
        
        self.attempts += 1
        self.save()
        
        if self.otp_code == code:
            self.is_verified = True
            self.verified_at = timezone.now()
            self.save()
            return True, "OTP verified successfully"
        
        remaining = self.max_attempts - self.attempts
        return False, f"Invalid OTP. {remaining} attempts remaining"
