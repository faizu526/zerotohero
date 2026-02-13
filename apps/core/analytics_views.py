"""
Analytics & Tracking Views for Zero To Hero
"""
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from apps.users.models import User
from apps.orders.models import Order
from apps.platforms.models import Product, Platform
from apps.affiliate.models import Affiliate, Commission


def is_staff_or_admin(user):
    """Check if user is staff or admin"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_admin)
def analytics_dashboard(request):
    """Admin Analytics Dashboard"""
    
    # Date ranges
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    last_90_days = today - timedelta(days=90)
    
    # ===== USER STATISTICS =====
    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    new_users_7d = User.objects.filter(date_joined__date__gte=last_7_days).count()
    new_users_30d = User.objects.filter(date_joined__date__gte=last_30_days).count()
    
    # User type distribution
    user_types = User.objects.values('user_type').annotate(count=Count('id'))
    
    # ===== ORDER STATISTICS =====
    total_orders = Order.objects.count()
    orders_today = Order.objects.filter(created_at__date=today).count()
    orders_7d = Order.objects.filter(created_at__date__gte=last_7_days).count()
    orders_30d = Order.objects.filter(created_at__date__gte=last_30_days).count()
    
    # Revenue statistics
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(
        total=Sum('total')
    )['total'] or 0
    
    revenue_today = Order.objects.filter(
        payment_status='paid',
        created_at__date=today
    ).aggregate(total=Sum('total'))['total'] or 0
    
    revenue_7d = Order.objects.filter(
        payment_status='paid',
        created_at__date__gte=last_7_days
    ).aggregate(total=Sum('total'))['total'] or 0
    
    revenue_30d = Order.objects.filter(
        payment_status='paid',
        created_at__date__gte=last_30_days
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # ===== PRODUCT STATISTICS =====
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    # Top selling products
    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:10]
    
    # ===== PLATFORM STATISTICS =====
    platform_stats = Platform.objects.annotate(
        product_count=Count('products'),
        order_count=Count('products__orderitem')
    ).order_by('-order_count')
    
    # ===== AFFILIATE STATISTICS =====
    total_affiliates = Affiliate.objects.count()
    total_commissions = Commission.objects.filter(status='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    pending_commissions = Commission.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # ===== CHART DATA =====
    # Daily orders for last 30 days
    daily_orders = Order.objects.filter(
        created_at__date__gte=last_30_days
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id'),
        revenue=Sum('total')
    ).order_by('date')
    
    # Monthly revenue for last 6 months
    six_months_ago = today - timedelta(days=180)
    monthly_revenue = Order.objects.filter(
        payment_status='paid',
        created_at__date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        revenue=Sum('total'),
        orders=Count('id')
    ).order_by('month')
    
    # Serialize data for JavaScript
    daily_orders_json = json.dumps(list(daily_orders), cls=DjangoJSONEncoder)
    user_types_json = json.dumps(list(user_types), cls=DjangoJSONEncoder)
    
    context = {
        # User stats
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_7d': new_users_7d,
        'new_users_30d': new_users_30d,
        'user_types': user_types_json,
        
        # Order stats
        'total_orders': total_orders,
        'orders_today': orders_today,
        'orders_7d': orders_7d,
        'orders_30d': orders_30d,
        
        # Revenue stats
        'total_revenue': total_revenue,
        'revenue_today': revenue_today,
        'revenue_7d': revenue_7d,
        'revenue_30d': revenue_30d,
        
        # Product stats
        'total_products': total_products,
        'active_products': active_products,
        'top_products': top_products,
        
        # Platform stats
        'platform_stats': platform_stats,
        
        # Affiliate stats
        'total_affiliates': total_affiliates,
        'total_commissions': total_commissions,
        'pending_commissions': pending_commissions,
        
        # Chart data
        'daily_orders': daily_orders_json,
        'monthly_revenue': json.dumps(list(monthly_revenue), cls=DjangoJSONEncoder),
        
        # Date range
        'date_range': f'{last_30_days} to {today}',
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def user_analytics(request):
    """Detailed User Analytics"""
    
    # User growth over time
    user_growth = User.objects.annotate(
        month=TruncMonth('date_joined')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Active users (logged in within last 30 days)
    last_30_days = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=last_30_days).count()
    
    # User retention (users who made at least 2 orders)
    repeat_customers = User.objects.annotate(
        order_count=Count('orders')
    ).filter(order_count__gte=2).count()
    
    context = {
        'user_growth': list(user_growth),
        'active_users': active_users,
        'repeat_customers': repeat_customers,
    }
    
    return render(request, 'admin/user_analytics.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def sales_analytics(request):
    """Detailed Sales Analytics"""
    
    # Sales by platform
    platform_sales = Platform.objects.annotate(
        total_sales=Sum('products__orderitem__order__total'),
        order_count=Count('products__orderitem__order')
    ).order_by('-total_sales')
    
    # Sales by date range
    today = timezone.now().date()
    date_ranges = {
        'today': today,
        'yesterday': today - timedelta(days=1),
        'last_7_days': today - timedelta(days=7),
        'last_30_days': today - timedelta(days=30),
        'this_month': today.replace(day=1),
    }
    
    sales_by_period = {}
    for period, start_date in date_ranges.items():
        sales_by_period[period] = Order.objects.filter(
            payment_status='paid',
            created_at__date__gte=start_date
        ).aggregate(
            revenue=Sum('total'),
            orders=Count('id')
        )
    
    context = {
        'platform_sales': platform_sales,
        'sales_by_period': sales_by_period,
    }
    
    return render(request, 'admin/sales_analytics.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def affiliate_analytics(request):
    """Affiliate Program Analytics"""
    
    # Top affiliates
    top_affiliates = Affiliate.objects.annotate(
        total_earned=Sum('commissions__amount'),
        referral_count=Count('commissions')
    ).order_by('-total_earned')[:20]
    
    # Commission statistics
    commission_stats = Commission.objects.values('status').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # Monthly affiliate growth
    monthly_affiliates = Affiliate.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    context = {
        'top_affiliates': top_affiliates,
        'commission_stats': commission_stats,
        'monthly_affiliates': list(monthly_affiliates),
    }
    
    return render(request, 'admin/affiliate_analytics.html', context)
