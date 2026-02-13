import stripe
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

# Stripe setup
stripe.api_key = settings.STRIPE_SECRET_KEY

# Razorpay setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def checkout(request):
    """Display checkout page"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart')
    
    # Calculate total
    total = 0
    for product_id, quantity in cart.items():
        total += 100 * quantity  # Placeholder price
    
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'total': total,
    }
    return render(request, 'payments/checkout.html', context)

@login_required
def process_payment(request):
    """Process Stripe payment"""
    if request.method != 'POST':
        return redirect('checkout')
    
    try:
        # Create PaymentIntent
        cart = request.session.get('cart', {})
        total = sum(100 * qty for qty in cart.values())  # Placeholder
        
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Convert to cents
            currency=settings.STRIPE_CURRENCY,
            metadata={'user_id': request.user.id},
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def payment_success(request):
    """Payment success page"""
    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.success(request, '🎉 Payment successful! Your order has been placed.')
    return render(request, 'payments/success.html')

def payment_cancel(request):
    """Payment cancelled page"""
    messages.info(request, 'Payment was cancelled.')
    return render(request, 'payments/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
        if event['type'] == 'payment_intent.succeeded':
            # Handle successful payment
            pass
            
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ===== RAZORPAY PAYMENT VIEWS =====

@login_required
def razorpay_checkout(request):
    """Display Razorpay checkout page"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart')
    
    # Calculate total in paise (INR smallest unit)
    total = 0
    for product_id, quantity in cart.items():
        total += 100 * quantity  # Placeholder price in INR
    
    # Create Razorpay order
    try:
        order_data = {
            'amount': int(total * 100),  # Convert to paise
            'currency': settings.RAZORPAY_CURRENCY,
            'payment_capture': 1,
            'notes': {
                'user_id': request.user.id,
                'user_email': request.user.email,
            }
        }
        razorpay_order = razorpay_client.order.create(order_data)
        
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_amount': order_data['amount'],
            'razorpay_currency': settings.RAZORPAY_CURRENCY,
            'user_name': request.user.get_full_name() or request.user.username,
            'user_email': request.user.email,
            'total': total,
        }
        return render(request, 'payments/razorpay_checkout.html', context)
        
    except Exception as e:
        messages.error(request, f'Error creating order: {str(e)}')
        return redirect('cart')

@login_required
@csrf_exempt
def razorpay_payment_verify(request):
    """Verify Razorpay payment signature"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Payment successful - clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({
            'status': 'success',
            'message': 'Payment verified successfully',
            'payment_id': razorpay_payment_id
        })
        
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid payment signature'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def razorpay_webhook(request):
    """Handle Razorpay webhooks"""
    webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
    
    try:
        payload = request.body
        signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
        
        # Verify webhook signature if secret is configured
        if webhook_secret:
            razorpay_client.utility.verify_webhook_signature(payload, signature, webhook_secret)
        
        data = json.loads(payload)
        event = data.get('event')
        
        if event == 'payment.captured':
            # Handle successful payment
            payment_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('id')
            # Update order status, send email, etc.
            pass
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
