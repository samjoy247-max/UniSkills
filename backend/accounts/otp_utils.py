"""
UN-60: OTP Utilities for Registration and Verification
"""

from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import TimeBasedOTP
import random
import string


def generate_otp():
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def create_and_send_otp(email):
    """Create OTP and send to email"""
    otp_code = generate_otp()
    
    # Delete existing OTPs for this email
    TimeBasedOTP.objects.filter(user_email=email).delete()
    
    # Create new OTP with 10-minute expiry
    otp_obj = TimeBasedOTP.objects.create(
        user_email=email,
        otp_code=otp_code,
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    
    # Try to send email
    try:
        send_mail(
            'UniSkills OTP Verification',
            f'Your OTP is: {otp_code}\n\nThis OTP expires in 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        # Fallback: print to console if email not configured
        print(f"[OTP] Email not configured. OTP for {email}: {otp_code}")
    
    return otp_obj


def verify_otp(email, otp_code):
    """Verify OTP for email"""
    try:
        otp_obj = TimeBasedOTP.objects.get(user_email=email, otp_code=otp_code)
        
        # Check if OTP is expired
        if timezone.now() > otp_obj.expires_at:
            otp_obj.delete()
            return False
        
        # OTP is valid
        otp_obj.delete()
        return True
    except TimeBasedOTP.DoesNotExist:
        return False
