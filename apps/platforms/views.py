from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count, Avg
from .models import Platform, Product, Bundle, PlatformCategory, ProductCategory

class PlatformListView(ListView):
    """500+ Platforms Listing"""
    model = Platform
    template_name = 'platforms/platforms.html'
    context_object_name = 'platforms'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Platform.objects.filter(is_active=True)
        
        # Search
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(country__icontains=q)
            )
        
        # Category Filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Commission Filter
        commission = self.request.GET.get('commission')
        if commission == 'free':
            queryset = queryset.filter(commission_rate=0)
        elif commission == '3':
            queryset = queryset.filter(commission_rate=3)
        elif commission == '5-7':
            queryset = queryset.filter(commission_rate__gte=5, commission_rate__lte=7)
        
        # Hidden Gems Filter
        if self.request.GET.get('hidden') == 'true':
            queryset = queryset.filter(is_hidden_gem=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PlatformCategory.objects.all()
        context['total_count'] = self.get_queryset().count()
        context['hidden_gems_count'] = Platform.objects.filter(is_hidden_gem=True).count()
        return context


class PlatformDetailView(DetailView):
    """Single Platform Page"""
    model = Platform
    template_name = 'platforms/platform-single.html'
    context_object_name = 'platform'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.filter(is_active=True)[:6]
        context['featured_products'] = self.object.products.filter(
            is_featured=True, 
            is_active=True
        )[:3]
        return context


class ProductListView(ListView):
    """1000+ Products Listing"""
    model = Product
    template_name = 'platforms/products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Search
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(platform__name__icontains=q)
            )
        
        # Category Filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Price Filter
        price = self.request.GET.get('price')
        if price == 'free':
            queryset = queryset.filter(is_free=True)
        elif price == 'under1000':
            queryset = queryset.filter(our_price__lt=1000)
        elif price == '1000-5000':
            queryset = queryset.filter(our_price__gte=1000, our_price__lte=5000)
        
        # Difficulty Filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['total_count'] = self.get_queryset().count()
        context['free_count'] = Product.objects.filter(is_free=True).count()
        return context


class ProductDetailView(DetailView):
    """Single Product Page"""
    model = Product
    template_name = 'platforms/product-single.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            platform=self.object.platform,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context


class BundleListView(ListView):
    """Course Bundles Listing"""
    model = Bundle
    template_name = 'platforms/bundles.html'
    context_object_name = 'bundles'
    
    def get_queryset(self):
        return Bundle.objects.filter(is_active=True).prefetch_related('products')


# Function-based view for backwards compatibility
def platform_detail_by_id(request, id):
    """Single Platform Page by ID - for backwards compatibility"""
    platform = get_object_or_404(Platform, id=id, is_active=True)
    products = platform.products.filter(is_active=True)[:6]
    featured_products = platform.products.filter(is_featured=True, is_active=True)[:3]
    
    context = {
        'platform': platform,
        'products': products,
        'featured_products': featured_products,
    }
    return render(request, 'platforms/platform-single.html', context)
