from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from apps.platforms.models import Platform, Product, Bundle
from apps.learning.models import HiddenGem

class HomeView(TemplateView):
    """Home Page - 3:3:3:3 Model"""
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Site Settings
        context['settings'] = SiteSettings.objects.first()
        
        # Featured Platforms (4 platforms)
        context['featured_platforms'] = Platform.objects.filter(
            is_featured=True, 
            is_active=True
        )[:4]
        
        # Featured Hidden Gems (4 gems)
        context['featured_gems'] = HiddenGem.objects.filter(
            is_featured=True,
            is_active=True
        )[:4]
        
        # Stats
        context['total_platforms'] = Platform.objects.filter(is_active=True).count()
        context['total_hidden_gems'] = HiddenGem.objects.filter(is_active=True).count()
        context['total_products'] = Product.objects.filter(is_active=True).count()
        
        return context


class AboutView(TemplateView):
    """About Page - Founder Story"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['founder'] = Founder.objects.first()
        context['missions'] = Mission.objects.all()
        context['impact_stats'] = ImpactStat.objects.all()
        return context


class ContactView(TemplateView):
    """Contact Page - Form Submission"""
    template_name = 'core/contact.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Thank you for contacting us! We will reply within 24 hours.')
        
        context = self.get_context_data()
        return render(request, self.template_name, context)


class FAQView(TemplateView):
    """FAQ Page"""
    template_name = 'core/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FAQCategory.objects.prefetch_related('faqs').filter(
            faqs__is_active=True
        ).distinct()
        return context


class BlogListView(ListView):
    """Blog Listing Page"""
    model = BlogPost
    template_name = 'core/blog.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category')


class BlogDetailView(DetailView):
    """Blog Single Page"""
    model = BlogPost
    template_name = 'core/blog-single.html'
    context_object_name = 'post'
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


# ===== AUTH VIEWS =====

def login_view(request):
    """Login Page - Supports both username and email login"""
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard-overview')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try to find user by email and authenticate
        if user is None and '@' in username_or_email:
            from apps.users.models import User
            try:
                # Case-insensitive email lookup
                user_by_email = User.objects.filter(email__iexact=username_or_email).first()
                if user_by_email:
                    user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard-overview')
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'auth/login.html')


def signup_view(request):
    """Signup Page"""
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard-overview')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Check for empty fields
        if not first_name or not last_name or not email or not password or not confirm_password:
            missing = []
            if not first_name: missing.append('First Name')
            if not last_name: missing.append('Last Name')
            if not email: missing.append('Email')
            if not password: missing.append('Password')
            if not confirm_password: missing.append('Confirm Password')
            messages.error(request, f'Please fill in all fields: {", ".join(missing)}')
            return render(request, 'auth/signup.html')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'auth/signup.html')
        
        from apps.users.models import User
        
        # Normalize email to lowercase
        email_lower = email.lower()
        
        # Check if email exists (case-insensitive)
        existing = User.objects.filter(email__iexact=email_lower).first()
        if existing:
            messages.error(request, 'An account with this email already exists. Please login.')
            return render(request, 'auth/signup.html')
        
        # Generate username from email
        username = email_lower.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username, 
                email=email_lower, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
            messages.error(request, f'Error creating account. Please try again.')
            return render(request, 'auth/signup.html')
        
        # Try to send welcome email (non-blocking)
        try:
            from .email_utils import send_welcome_email
            send_welcome_email(user)
        except Exception as e:
            pass  # Email failure shouldn't stop signup
        
        # Authenticate and login the user properly
        from django.contrib.auth import authenticate, login as auth_login
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f'Welcome {first_name}! Your account has been created successfully.')
            return redirect('dashboard-overview')
        else:
            # If authentication fails, still show success but ask to login
            messages.success(request, f'Account created! Please login with your email and password.')
            return redirect('login')
    
    return render(request, 'auth/signup.html')


def logout_view(request):
    """Logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def forgot_password_view(request):
    """Forgot Password Page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, 'If an account exists with this email, you will receive a password reset link.')
        return render(request, 'auth/forgot-password.html')
    
    return render(request, 'auth/forgot-password.html')


# ===== SEARCH VIEW =====

def search_view(request):
    """Search across platforms, products, and hidden gems"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'core/search.html', {
            'query': '',
            'platforms': [],
            'products': [],
            'hidden_gems': [],
            'total_results': 0
        })
    
    # Search in platforms
    platforms = Platform.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()[:10]
    
    # Search in products/courses
    products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(platform__name__icontains=query)
    ).distinct()[:10]
    
    # Search in hidden gems
    hidden_gems = HiddenGem.objects.filter(
        is_active=True
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    ).distinct()[:10]
    
    total_results = platforms.count() + products.count() + hidden_gems.count()
    
    return render(request, 'core/search.html', {
        'query': query,
        'platforms': platforms,
        'products': products,
        'hidden_gems': hidden_gems,
        'total_results': total_results
    })
