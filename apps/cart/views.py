from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.platforms.models import Product

def cart_view(request):
    """Display the shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            item_total = product.our_price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total += item_total
        except Product.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': len(cart_items),
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    """Add a product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    
    messages.success(request, f'✅ {product.name} added to cart!')
    return redirect('cart')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item removed from cart')
    
    return redirect('cart')

def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        if quantity > 0:
            cart[str(item_id)] = quantity
        else:
            del cart[str(item_id)]
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart')

def clear_cart(request):
    """Clear entire cart"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared')
    return redirect('cart')
