"""
UN-64: Session History and Profile Picture Upload
- session_history: Shows all completed sessions for the current user
- Profile picture handled in profile.py
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Booking, SessionHistory


@login_required
def session_history(request):
    """
    UN-64: Show session history for the current user.
    - Students see sessions they attended
    - Instructors see sessions they taught
    """
    user = request.user

    if user.role == "student":
        # Get accepted/completed bookings for this student that have session records
        sessions = SessionHistory.objects.filter(
            booking__student=user
        ).select_related('booking', 'booking__skill_post', 'booking__skill_post__provider')
        page_title = "My Session History"

    else:
        # Instructor: sessions for skills they teach
        sessions = SessionHistory.objects.filter(
            booking__skill_post__provider=user
        ).select_related('booking', 'booking__student', 'booking__skill_post')
        page_title = "Sessions I've Taught"

    context = {
        'sessions': sessions,
        'page_title': page_title,
        'total_sessions': sessions.count(),
        'attended_count': sessions.filter(attendance_status='attended').count(),
    }
    return render(request, 'accounts/session_history.html', context)
