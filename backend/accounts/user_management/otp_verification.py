"""
OTP Verification Flow
Handles email verification via OTP after registration
"""

from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from ..otp_utils import verify_otp, create_and_send_otp

User = get_user_model()


class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp_code = forms.CharField(
        label="OTP Code",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP',
            'autocomplete': 'off',
            'inputmode': 'numeric',
        })
    )

    def clean_otp_code(self):
        otp = self.cleaned_data['otp_code'].strip()
        if not otp.isdigit():
            raise forms.ValidationError("OTP must contain only digits")
        return otp


def verify_email_otp(request):
    """Handle OTP verification after registration"""
    email = request.session.get('pending_verification_email')
    
    if not email:
        messages.error(request, "No pending verification. Please register first.")
        return redirect('accounts:register_student')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            
            # Verify OTP
            if verify_otp(email, otp_code):
                # Mark user as email verified
                user = User.objects.filter(email=email).order_by("-id").first()
                if not user:
                    messages.error(request, "User not found.")
                    return redirect('accounts:register_student')

                user.is_email_verified = True
                user.save()

                # Clear session
                if 'pending_verification_email' in request.session:
                    del request.session['pending_verification_email']

                messages.success(request, "Email verified successfully! You can now log in.")
                return redirect('accounts:login')
            else:
                messages.error(request, "Invalid or expired OTP. Please try again.")
                form.add_error('otp_code', 'Invalid OTP')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_email_otp.html', {
        'form': form,
        'email': email,
    })


def resend_otp(request):
    """Resend OTP to email"""
    email = request.session.get('pending_verification_email')
    
    if not email:
        messages.error(request, "No pending verification.")
        return redirect('accounts:register_student')
    
    user = User.objects.filter(email=email).order_by("-id").first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('accounts:register_student')

    create_and_send_otp(email)
    messages.success(request, f"OTP resent to {email}. Check your email or console for the OTP code.")
    return redirect('accounts:verify_email_otp')
