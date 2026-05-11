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
        subject = 'UniSkills Email Verification OTP'
        message = f'''
Hello,

Your UniSkills Email Verification OTP is: {otp_code}

This OTP will expire in 10 minutes.

If you did not request this OTP, please ignore this email.

Best regards,
UniSkills Team
        '''
        
        html_message = f'''
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #333;">UniSkills Email Verification</h2>
        <p>Hello,</p>
        <p>Your verification OTP is:</p>
        <div style="background: #f0f0f0; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
            <h1 style="color: #667eea; letter-spacing: 5px; margin: 0;">{otp_code}</h1>
        </div>
        <p style="color: #666; font-size: 14px;">This OTP will expire in 10 minutes.</p>
        <p style="color: #666; font-size: 14px;">If you did not request this OTP, please ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
        <p style="color: #999; font-size: 12px;">© 2026 UniSkills - University of Asia Pacific</p>
    </body>
</html>
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"[EMAIL SENT] OTP sent to {email}")
    except Exception as e:
        # Fallback: print to console if email fails
        print(f"[EMAIL ERROR] Failed to send OTP to {email}: {str(e)}")
        print(f"[OTP] OTP for {email}: {otp_code}")
    
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

