
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from decimal import Decimal
from apps.orders.models import Order
from apps.users.models import Enrollment, Wishlist

# ===== DASHBOARD VIEWS =====

@login_required
def dashboard_overview(request):
    # Get user's orders statistics
    orders = Order.objects.filter(user=request.user)
    total_spent = orders.filter(payment_status='paid').aggregate(Sum('total'))['total__sum'] or Decimal('0')
    total_saved = total_spent * Decimal('0.06')  # 6% average savings
    commission_earned = orders.filter(payment_status='paid').aggregate(Sum('affiliate_commission'))['affiliate_commission__sum'] or Decimal('0')
    
    # Get course statistics using Enrollment
    enrollments = Enrollment.objects.filter(user=request.user)
    total_courses = enrollments.count()
    in_progress = enrollments.filter(status='active').count()
    completed = enrollments.filter(status='completed').count()
    
    # Recent orders (last 5)
    recent_orders = orders.order_by('-created_at')[:5]
    
    # Recent enrollments (last 5)
    recent_courses = enrollments.order_by('-enrolled_at')[:5]
    
    context = {
        'total_spent': total_spent,
        'total_saved': total_saved,
        'commission_earned': commission_earned,
        'total_courses': total_courses,
        'in_progress': in_progress,
        'completed': completed,
        'recent_orders': recent_orders,
        'recent_courses': recent_courses,
    }
    return render(request, 'users/dashboard/overview.html', context)

@login_required
def dashboard_my_courses(request):
    # Get all user's enrollments with filtering
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-enrolled_at')
    
    # Get filter from query params
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        enrollments = enrollments.filter(status=status_filter)
    
    # Calculate statistics
    total_courses = enrollments.count()
    in_progress = enrollments.filter(status='active').count()
    completed = enrollments.filter(status='completed').count()
    
    context = {
        'enrollments': enrollments,
        'total_courses': total_courses,
        'in_progress': in_progress,
        'completed': completed,
        'status_filter': status_filter,
    }
    return render(request, 'users/dashboard/my-courses.html', context)

@login_required
def dashboard_orders(request):
    # Get all user's orders
    orders = Order.objects.filter(user=request.user)
    
    # Search functionality - Search by Order Number
    search_query = request.GET.get('search', '').strip()
    if search_query:
        orders = orders.filter(order_number__icontains=search_query)
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    
    # Payment status filter
    payment_status = request.GET.get('payment_status', '')
    if payment_status:
        orders = orders.filter(payment_status=payment_status)
    
    # Date range filter
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        from datetime import datetime
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d')
            orders = orders.filter(created_at__date__gte=date_from_parsed)
        except ValueError:
            pass
    
    if date_to:
        from datetime import datetime
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d')
            orders = orders.filter(created_at__date__lte=date_to_parsed)
        except ValueError:
            pass
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sort_fields = ['created_at', '-created_at', 'total', '-total', 'order_number', '-order_number']
    if sort_by in valid_sort_fields:
        orders = orders.order_by(sort_by)
    else:
        orders = orders.order_by('-created_at')
    
    # Calculate statistics (based on filtered results)
    total_spent = orders.filter(payment_status='paid').aggregate(Sum('total'))['total__sum'] or Decimal('0')
    total_saved = total_spent * Decimal('0.06')
    commission_earned = orders.filter(payment_status='paid').aggregate(Sum('affiliate_commission'))['affiliate_commission__sum'] or Decimal('0')
    
    context = {
        'orders': orders,
        'total_spent': total_spent,
        'total_saved': total_saved,
        'commission_earned': commission_earned,
        'search_query': search_query,
        'status_filter': status_filter,
        'payment_status': payment_status,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
    }
    return render(request, 'users/dashboard/orders.html', context)

@login_required
def dashboard_wishlist(request):
    # Get user's wishlist
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'users/dashboard/wishlist.html', context)

@login_required
def dashboard_settings(request):
    from apps.users.models import UserSettings
    # Get or create settings
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update settings
        user_settings.theme = request.POST.get('theme', 'light')
        user_settings.language = request.POST.get('language', 'en')
        user_settings.email_course_updates = request.POST.get('email_course_updates') == 'on'
        user_settings.email_promotions = request.POST.get('email_promotions') == 'on'
        user_settings.email_affiliate = request.POST.get('email_affiliate') == 'on'
        user_settings.profile_public = request.POST.get('profile_public') == 'on'
        user_settings.show_wishlist = request.POST.get('show_wishlist') == 'on'
        user_settings.show_certificates = request.POST.get('show_certificates') == 'on'
        user_settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('dashboard-settings')
    
    return render(request, 'users/dashboard/settings.html', {'user_settings': user_settings})

@login_required
def dashboard_affiliate(request):
    from apps.affiliate.models import Affiliate, Commission, Withdrawal
    
    # Get or create affiliate profile
    try:
        affiliate = request.user.affiliate_profile
    except Affiliate.DoesNotExist:
        affiliate = None
    
    # Get commission statistics
    if affiliate:
        total_commission = Commission.objects.filter(affiliate=affiliate, status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
        pending_commission = Commission.objects.filter(affiliate=affiliate, status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawals = affiliate.withdrawals.all()[:5]
    else:
        total_commission = 0
        pending_commission = 0
        withdrawals = []
    
    context = {
        'affiliate': affiliate,
        'total_commission': total_commission,
        'pending_commission': pending_commission,
        'withdrawals': withdrawals,
        'affiliate_code': request.user.affiliate_code or 'Not generated',
    }
    return render(request, 'users/dashboard/affiliate.html', context)
