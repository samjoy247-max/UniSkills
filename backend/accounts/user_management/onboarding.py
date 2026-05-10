"""
UN-77: Alumni Onboarding
Alumni registration, welcome flow, profile setup
"""

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()


def register_alumni_user(username, email, password, full_name='', graduation_year=None):
    """UN-77: Register new alumni user"""
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name.split()[0] if full_name else '',
            last_name=full_name.split()[-1] if full_name else '',
            role='alumni',
            graduation_year=graduation_year,
        )
        return user, True
    except Exception as e:
        return None, False


def send_alumni_welcome_email(user):
    """UN-77: Send welcome email to new alumni"""
    subject = 'Welcome to UniSkills Alumni Network!'
    
    html_message = f"""
    <html>
        <body>
            <h2>Welcome, {user.first_name}!</h2>
            <p>You're now part of the UniSkills Alumni Network.</p>
            <p>Complete your profile and share your career journey with fellow alumni.</p>
            <ul>
                <li>Edit your profile at: /alumni/profile/</li>
                <li>Create career posts at: /alumni/posts/create/</li>
                <li>Browse alumni directory at: /alumni/directory/</li>
            </ul>
            <p>Best regards,<br>UniSkills Team</p>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        'noreply@uniskills.dev',
        [user.email],
        html_message=html_message,
        fail_silently=True
    )


def get_onboarding_checklist(user):
    """UN-77: Get alumni onboarding progress checklist"""
    profile_complete = bool(user.current_company and user.graduation_year)
    profile_picture_added = bool(user.profile_picture)
    first_post_created = user.alumni_posts.exists()
    
    return {
        'profile_complete': profile_complete,
        'profile_picture_added': profile_picture_added,
        'first_post_created': first_post_created,
        'progress_percentage': sum([profile_complete, profile_picture_added, first_post_created]) * 33,
        'next_step': 'Complete your profile' if not profile_complete else 'Add profile picture' if not profile_picture_added else 'Create your first post',
    }


def complete_alumni_onboarding(user, company, graduation_year, bio=''):
    """UN-77: Complete alumni onboarding flow"""
    user.current_company = company
    user.graduation_year = graduation_year
    user.bio = bio
    user.is_alumni_verified = True
    user.save()
    return user


def get_alumni_onboarding_stats():
    """UN-77: Get onboarding statistics"""
    total_registered = User.objects.filter(role='alumni').count()
    profile_completed = User.objects.filter(role='alumni', current_company__isnull=False).count()
    posts_created = User.objects.filter(role='alumni', alumni_posts__isnull=False).distinct().count()
    
    return {
        'total_alumni_registered': total_registered,
        'completed_profiles': profile_completed,
        'with_posts': posts_created,
        'onboarding_rate': (profile_completed / total_registered * 100) if total_registered > 0 else 0,
    }


def send_onboarding_reminder(user):
    """UN-77: Send reminder to incomplete onboarding"""
    checklist = get_onboarding_checklist(user)
    if checklist['progress_percentage'] < 100:
        subject = 'Complete Your Alumni Profile'
        html_message = f"""
        <html>
            <body>
                <h3>Hi {user.first_name},</h3>
                <p>You're {checklist['progress_percentage']}% through your alumni profile setup.</p>
                <p>Next: {checklist['next_step']}</p>
                <p><a href="/alumni/onboarding/">Continue Setup</a></p>
            </body>
        </html>
        """
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            'noreply@uniskills.dev',
            [user.email],
            html_message=html_message,
            fail_silently=True
        )


def get_alumni_cohort(graduation_year):
    """UN-77: Get cohort of alumni from same graduation year"""
    return User.objects.filter(
        role='alumni',
        graduation_year=graduation_year
    ).order_by('username')
