"""
Email Utility Functions for Zero To Hero
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = '🚀 Welcome to Zero To Hero!'
    
    # Render email template
    html_message = render_to_string('emails/welcome_email.html', {
        'user': user,
        'dashboard_url': f"{settings.BASE_URL}/dashboard/overview/" if hasattr(settings, 'BASE_URL') else '/dashboard/overview/',
    })
    
    # Create plain text version
    plain_message = strip_tags(html_message)
    
    # Send email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False


def send_order_confirmation_email(user, order, payment_id=None):
    """Send order confirmation email"""
    subject = f'🎉 Order Confirmed! #{order.id}'
    
    # Get order items
    order_items = []
    total_amount = 0
    
    # This is a placeholder - adjust based on your Order model structure
    if hasattr(order, 'items'):
        for item in order.items.all():
            order_items.append({
                'name': item.product.name if hasattr(item, 'product') else 'Course',
                'price': item.price if hasattr(item, 'price') else item.product.price
            })
            total_amount += item.price if hasattr(item, 'price') else item.product.price
    
    # Render email template
    html_message = render_to_string('emails/order_confirmation.html', {
        'user': user,
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount,
        'payment_id': payment_id or 'N/A',
        'order_date': order.created_at.strftime('%B %d, %Y') if hasattr(order, 'created_at') else 'Today',
        'my_courses_url': f"{settings.BASE_URL}/dashboard/my-courses/" if hasattr(settings, 'BASE_URL') else '/dashboard/my-courses/',
        'support_url': f"{settings.BASE_URL}/contact/" if hasattr(settings, 'BASE_URL') else '/contact/',
        'affiliate_link': f"{settings.BASE_URL}/?ref={user.affiliate_code}" if hasattr(settings, 'BASE_URL') else f'/?ref={user.affiliate_code}',
    })
    
    # Create plain text version
    plain_message = strip_tags(html_message)
    
    # Send email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending order confirmation email: {e}")
        return False


def send_course_enrollment_email(user, enrollment):
    """Send course enrollment confirmation email"""
    subject = f'🎓 You\'re enrolled! {enrollment.product.name}'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">🎓 Course Enrollment Confirmed!</h2>
            
            <p>Hi {user.first_name},</p>
            
            <p>You're now enrolled in <strong>{enrollment.product.name}</strong>!</p>
            
            <div style="background: #f0f9ff; padding: 15px; border-left: 4px solid #2563eb; margin: 20px 0;">
                <strong>Course Details:</strong><br>
                Course: {enrollment.product.name}<br>
                Enrolled: {enrollment.enrolled_at.strftime('%B %d, %Y')}<br>
                Status: Active
            </div>
            
            <p><a href="/dashboard/my-courses/" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;">Start Learning →</a></p>
            
            <p>Happy learning!<br>Zero To Hero Team</p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending enrollment email: {e}")
        return False


def send_password_reset_email(user, reset_url):
    """Send password reset email"""
    subject = '🔐 Password Reset Request - Zero To Hero'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">🔐 Password Reset</h2>
            
            <p>Hi {user.first_name or user.username},</p>
            
            <p>You requested a password reset for your Zero To Hero account.</p>
            
            <p>Click the button below to reset your password:</p>
            
            <p><a href="{reset_url}" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;">Reset Password →</a></p>
            
            <p style="color: #666; font-size: 14px;">If you didn't request this, please ignore this email. The link will expire in 24 hours.</p>
            
            <p>Best regards,<br>Zero To Hero Team</p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False
