"""
UN-81: Alumni Profiles and Posts
Alumni profile management, post creation, profile enrichment
"""

from django.db import models
from accounts.models import CustomUser, AlumniPost


def create_alumni_profile(user, bio='', company='', position='', graduation_year=None):
    """UN-81: Create/update alumni profile"""
    user.current_company = company
    user.graduation_year = graduation_year
    user.is_alumni_verified = True
    user.role = 'alumni'
    user.save()
    return user


def get_alumni_profile(user):
    """UN-81: Get alumni profile details"""
    if not user.is_alumni_verified:
        return None
    
    return {
        'username': user.username,
        'email': user.email,
        'company': user.current_company,
        'graduation_year': user.graduation_year,
        'posts_count': AlumniPost.objects.filter(author=user, status='approved').count(),
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
        'joined_date': user.date_joined,
    }


def get_alumni_directory(limit=50):
    """UN-81: Get directory of all verified alumni"""
    alumni_users = CustomUser.objects.filter(is_alumni_verified=True, role='alumni').prefetch_related('alumni_posts')
    alumni_list = []
    for user in alumni_users[:limit]:
        alumni_list.append({
            'id': user.id,
            'username': user.username,
            'company': user.current_company,
            'graduation_year': user.graduation_year,
            'posts_count': user.alumni_posts.filter(status='approved').count(),
        })
    return alumni_list


def search_alumni(keyword):
    """UN-81: Search alumni by name, company, or major"""
    return CustomUser.objects.filter(
        is_alumni_verified=True,
        role='alumni'
    ).filter(
        models.Q(username__icontains=keyword) |
        models.Q(current_company__icontains=keyword) |
        models.Q(major__icontains=keyword)
    )


def get_alumni_posts(user):
    """UN-81: Get all posts by alumni user"""
    return AlumniPost.objects.filter(
        author=user,
        status='approved'
    ).order_by('-created_at')


def create_alumni_post(user, title, content, category='career'):
    """UN-81: Create alumni post"""
    post = AlumniPost.objects.create(
        author=user,
        title=title,
        content=content,
        status='pending'
    )
    return post


def get_alumni_stats():
    """UN-81: Get alumni network statistics"""
    total_alumni = CustomUser.objects.filter(is_alumni_verified=True).count()
    total_posts = AlumniPost.objects.filter(status='approved').count()
    active_alumni = AlumniPost.objects.filter(status='approved').values('author').distinct().count()
    
    return {
        'total_alumni': total_alumni,
        'active_alumni': active_alumni,
        'total_posts': total_posts,
        'companies_represented': CustomUser.objects.filter(is_alumni_verified=True).values('current_company').distinct().count(),
    }


def verify_alumni_account(user):
    """UN-81: Verify user as alumni (admin action)"""
    user.is_alumni_verified = True
    user.role = 'alumni'
    user.save()
    return user


def get_alumni_by_company(company):
    """UN-81: Get all alumni from specific company"""
    return CustomUser.objects.filter(
        is_alumni_verified=True,
        current_company=company
    ).order_by('username')


def get_alumni_by_graduation_year(year):
    """UN-81: Get all alumni from specific graduation year"""
    return CustomUser.objects.filter(
        is_alumni_verified=True,
        graduation_year=year
    ).order_by('username')
