#!/usr/bin/env python
"""
Test SMTP Email Configuration
Tests both Console and actual SMTP backends
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniskills_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 80)
print("📧 UNISKILLS EMAIL CONFIGURATION TEST")
print("=" * 80)

# Show current configuration
print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else '(not configured)'}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Test 1: Console Backend (Development)
print("\n" + "=" * 80)
print("TEST 1: Console Backend Email (Development)")
print("=" * 80)

try:
    subject = "🎉 UniSkills Test Email - Console Backend"
    message = """
    Hello UniSkills Team!
    
    This is a test email sent via Console Backend.
    
    If you're seeing this in the console output instead of your inbox,
    the console backend is working correctly!
    
    Features tested:
    - Email subject
    - Email body
    - Sender address
    - Recipient address
    
    Best regards,
    UniSkills Development Team
    """
    
    recipient_email = "23101102@uap-bd.edu"  # Joy's email
    
    sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )
    
    if sent:
        print(f"✅ Email sent successfully (1 message)")
        print(f"   To: {recipient_email}")
        print(f"   Subject: {subject}")
        print(f"   (Check console output above for email body)")
    else:
        print(f"❌ Email failed to send")
        
except Exception as e:
    print(f"❌ Error sending email: {e}")
    import traceback
    traceback.print_exc()

# Test 2: OTP Email Simulation
print("\n" + "=" * 80)
print("TEST 2: OTP Email Simulation")
print("=" * 80)

try:
    otp_code = "123456"
    subject = "🔐 Your UniSkills OTP Code"
    message = f"""
    Welcome to UniSkills!
    
    Your One-Time Password (OTP) for email verification is:
    
    ╔═══════════════════════╗
    ║  OTP: {otp_code}          ║
    ║  Valid for: 10 minutes ║
    ╚═══════════════════════╝
    
    This code will expire in 10 minutes.
    If you didn't request this code, please ignore this email.
    
    Best regards,
    UniSkills Team
    """
    
    sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["test@example.com"],
        fail_silently=False,
    )
    
    if sent:
        print(f"✅ OTP email simulation sent successfully")
    else:
        print(f"❌ OTP email failed to send")
        
except Exception as e:
    print(f"❌ Error sending OTP email: {e}")

# Test 3: Booking Confirmation Email Simulation
print("\n" + "=" * 80)
print("TEST 3: Booking Confirmation Email Simulation")
print("=" * 80)

try:
    subject = "✅ Booking Request Confirmed - UniSkills"
    message = """
    Hello Student,
    
    Your booking request has been received!
    
    Booking Details:
    - Skill: Advanced Django Development
    - Provider: Shahin Akand
    - Requested Date: May 20, 2026
    - Duration: 2 hours
    - Fee: ৳500
    
    Status: ⏳ Waiting for provider to accept
    
    You'll receive an email notification once the provider responds.
    
    Best regards,
    UniSkills Team
    """
    
    sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["student@example.com"],
        fail_silently=False,
    )
    
    if sent:
        print(f"✅ Booking confirmation email simulation sent successfully")
    else:
        print(f"❌ Booking email failed to send")
        
except Exception as e:
    print(f"❌ Error sending booking email: {e}")

# Summary
print("\n" + "=" * 80)
print("📊 SUMMARY")
print("=" * 80)

if "console" in settings.EMAIL_BACKEND.lower():
    print("\n✅ Development Email Backend (Console)")
    print("   Emails are printed to console, not sent")
    print("   Perfect for testing without production email")
    print("\n⚠️  To enable real SMTP:")
    print("   1. Update .env:")
    print("      EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
    print("      EMAIL_HOST_USER=your-gmail@gmail.com")
    print("      EMAIL_HOST_PASSWORD=your-app-password")
    print("   2. Use Gmail App Password (not regular password)")
    print("   3. Enable 'Less secure app access' if using regular Gmail account")
else:
    print("\n✅ Production Email Backend (SMTP)")
    print("   Emails are sent via actual SMTP server")

print("\n✓ Email configuration test completed!")
print("=" * 80)
