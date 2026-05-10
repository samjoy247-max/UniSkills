"""
UN-91: Basic Stats and Analytics
Platform statistics, dashboard metrics, usage analytics
"""

from django.db.models import Count, Avg, Q
from accounts.models import CustomUser, SkillPost, Booking, Rating, AlumniPost, SessionHistory


def get_platform_stats():
    """UN-91: Get overall platform statistics"""
    return {
        'total_users': CustomUser.objects.count(),
        'total_providers': CustomUser.objects.filter(role='provider').count(),
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_alumni': CustomUser.objects.filter(role='alumni').count(),
        'total_skills': SkillPost.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_sessions': SessionHistory.objects.count(),
        'total_ratings': Rating.objects.count(),
        'total_alumni_posts': AlumniPost.objects.count(),
    }


def get_booking_stats():
    """UN-91: Get booking statistics"""
    total_bookings = Booking.objects.count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    return {
        'total': total_bookings,
        'completed': completed_bookings,
        'pending': pending_bookings,
        'cancelled': cancelled_bookings,
        'completion_rate': (completed_bookings / total_bookings * 100) if total_bookings > 0 else 0,
    }


def get_skill_stats():
    """UN-91: Get skill statistics"""
    total_skills = SkillPost.objects.count()
    active_skills = SkillPost.objects.filter(status='active').count()
    avg_rating = Rating.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = Rating.objects.count()
    
    return {
        'total_skills': total_skills,
        'active_skills': active_skills,
        'average_rating': round(avg_rating, 2),
        'total_reviews': total_reviews,
        'top_rated_skills': list(
            SkillPost.objects.annotate(
                avg_rating=Avg('ratings__rating'),
                review_count=Count('ratings')
            ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5].values(
                'id', 'title', 'avg_rating', 'review_count'
            )
        )
    }


def get_user_engagement_stats():
    """UN-91: Get user engagement metrics"""
    active_users = CustomUser.objects.filter(
        Q(bookings_made__isnull=False) | Q(alumni_posts__isnull=False) | Q(ratings_given__isnull=False)
    ).distinct().count()
    
    total_users = CustomUser.objects.count()
    engagement_rate = (active_users / total_users * 100) if total_users > 0 else 0
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'engagement_rate': round(engagement_rate, 2),
    }


def get_session_stats():
    """UN-91: Get session statistics"""
    total_sessions = SessionHistory.objects.count()
    attended_sessions = SessionHistory.objects.filter(attendance_status='attended').count()
    
    return {
        'total_sessions': total_sessions,
        'attended': attended_sessions,
        'attendance_rate': (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0,
    }


def get_alumni_stats():
    """UN-91: Get alumni network statistics"""
    total_alumni = CustomUser.objects.filter(role='alumni').count()
    posts_created = AlumniPost.objects.count()
    approved_posts = AlumniPost.objects.filter(status='approved').count()
    
    return {
        'total_alumni': total_alumni,
        'total_posts': posts_created,
        'approved_posts': approved_posts,
        'engagement_rate': (total_alumni / CustomUser.objects.count() * 100) if CustomUser.objects.count() > 0 else 0,
    }


def get_revenue_stats():
    """UN-91: Get revenue statistics (if paid skills enabled)"""
    paid_skills = SkillPost.objects.filter(fee__gt=0).count()
    completed_paid_bookings = Booking.objects.filter(
        status='completed',
        skill_post__fee__gt=0
    ).count()
    total_potential_revenue = sum(
        Booking.objects.filter(status='completed', skill_post__fee__gt=0).values_list('skill_post__fee', flat=True)
    )
    
    return {
        'paid_skills': paid_skills,
        'completed_paid_sessions': completed_paid_bookings,
        'total_revenue': total_potential_revenue,
    }


def get_top_providers():
    """UN-91: Get top providers by rating and sessions"""
    return list(
        CustomUser.objects.filter(role='provider').annotate(
            skill_count=Count('skill_posts'),
            avg_rating=Avg('skill_posts__ratings__rating'),
            total_bookings=Count('skill_posts__bookings')
        ).filter(skill_count__gt=0).order_by('-avg_rating')[:10].values(
            'id', 'username', 'skill_count', 'avg_rating', 'total_bookings'
        )
    )


def get_dashboard_summary():
    """UN-91: Get complete dashboard summary"""
    return {
        'platform': get_platform_stats(),
        'bookings': get_booking_stats(),
        'skills': get_skill_stats(),
        'engagement': get_user_engagement_stats(),
        'sessions': get_session_stats(),
        'alumni': get_alumni_stats(),
        'top_providers': get_top_providers(),
    }
