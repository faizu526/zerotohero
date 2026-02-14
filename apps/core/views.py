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
    if request.method == 'POST':
        # DEBUG: Print all POST data received
        print(f"\n=== SIGNUP DEBUG ===")
        print(f"POST data keys: {list(request.POST.keys())}")
        print(f"Full POST data: {dict(request.POST)}")
        
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        print(f"Extracted values:")
        print(f"  first_name: '{first_name}' (len={len(first_name)})")
        print(f"  last_name: '{last_name}' (len={len(last_name)})")
        print(f"  email: '{email}' (len={len(email)})")
        print(f"  password: {'*' * len(password)} (len={len(password)})")
        print(f"  confirm_password: {'*' * len(confirm_password)} (len={len(confirm_password)})")
        
        # Check for empty fields
        if not first_name or not last_name or not email or not password or not confirm_password:
            missing = []
            if not first_name: missing.append('first_name')
            if not last_name: missing.append('last_name')
            if not email: missing.append('email')
            if not password: missing.append('password')
            if not confirm_password: missing.append('confirm_password')
            print(f"ERROR: Missing fields: {missing}")
            messages.error(request, f'Please fill in all fields. Missing: {", ".join(missing)}')
            return render(request, 'auth/signup.html')
        
        # Validation
        if password != confirm_password:
            print(f"ERROR: Password mismatch!")
            print(f"  password: {repr(password)}")
            print(f"  confirm: {repr(confirm_password)}")
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')
        
        if len(password) < 8:
            print(f"ERROR: Password too short ({len(password)} chars)")
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'auth/signup.html')
        
        from apps.users.models import User
        
        # Normalize email to lowercase
        email_lower = email.lower()
        print(f"Normalized email: '{email_lower}'")
        
        # Check if email exists (case-insensitive)
        existing = User.objects.filter(email__iexact=email_lower).first()
        if existing:
            print(f"ERROR: Email already exists! Found: {existing.email} (ID: {existing.id})")
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/signup.html')
        
        print("Email is unique, proceeding...")
        
        # Generate username from email
        username = email_lower.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        print(f"Generated username: '{username}'")
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username, 
                email=email_lower, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print(f"SUCCESS: User created! ID: {user.id}, Username: {user.username}")
        except Exception as e:
            print(f"ERROR creating user: {str(e)}")
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')
        
        # Try to send welcome email
        try:
            from .email_utils import send_welcome_email
            send_welcome_email(user)
            print("Welcome email sent")
        except Exception as e:
            print(f"Welcome email error: {e}")
        
        login(request, user)
        messages.success(request, 'Account created successfully! Welcome to your dashboard.')
        print("=== SIGNUP COMPLETE ===\n")
        return redirect('home')
    
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
