"""
Booking system for skill sessions (UN-60, UN-64)
Handles creating, responding, and managing skill session bookings
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.utils import timezone

from ..models import Booking, SkillPost, SessionHistory
from django.forms import ModelForm, Textarea, TextInput


def get_booking_scheduled_datetime(booking):
    """Return the datetime that should be used to judge rating availability."""
    return booking.requested_date or booking.skill_post.available_time


def booking_can_be_rated(booking):
    """Allow rating after completion or once the scheduled time has passed."""
    scheduled_at = get_booking_scheduled_datetime(booking)
    if booking.status == Booking.STATUS_COMPLETED:
        return True
    if booking.status != Booking.STATUS_ACCEPTED:
        return False
    return bool(scheduled_at and scheduled_at <= timezone.now())


class BookingForm(ModelForm):
    """Form for creating booking requests"""
    class Meta:
        model = Booking
        fields = ['message', 'requested_date']
        widgets = {
            'message': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your booking message here...'
            }),
            'requested_date': TextInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'When would you like to schedule this?'
            })
        }


class BookingDecisionForm(ModelForm):
    """Form for instructor decision on bookings"""
    class Meta:
        model = Booking
        fields = ['status', 'decline_reason']
        widgets = {
            'decline_reason': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why are you declining this request?'
            })
        }


@login_required
def create_booking(request, post_id):
    """Create a booking request for a skill post (UN-60)"""
    skill_post = get_object_or_404(SkillPost, id=post_id, status=SkillPost.STATUS_APPROVED)
    
    # Student cannot book their own posts
    if skill_post.provider == request.user:
        messages.error(request, "You cannot book your own skill posts")
        return redirect("accounts:skill_detail", post_id=post_id)
    
    # Check if already has an ACTIVE booking (pending or accepted)
    existing_booking = Booking.objects.filter(
        student=request.user,
        skill_post=skill_post,
        status__in=[Booking.STATUS_PENDING, Booking.STATUS_ACCEPTED]
    ).first()
    
    if existing_booking:
        messages.warning(request, "You already have an active booking for this skill. Cancel or wait for the current one to be resolved before re-booking.")
        return redirect("accounts:bookings")
    
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.skill_post = skill_post
            booking.status = Booking.STATUS_PENDING
            booking.save()
            
            messages.success(request, "Booking request sent! Waiting for instructor approval...")
            return redirect("accounts:bookings")
    else:
        form = BookingForm()
    
    return render(request, "accounts/create_booking.html", {
        "form": form,
        "skill_post": skill_post,
        "page_title": f"Book: {skill_post.title}"
    })


@login_required
def respond_booking(request, booking_id):
    """Instructor responds to booking request (accept/decline) (UN-60)"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only the skill post provider (instructor) can respond
    if booking.skill_post.provider != request.user:
        return HttpResponseForbidden("You cannot respond to this booking")
    
    if booking.status != Booking.STATUS_PENDING:
        messages.error(request, "This booking has already been responded to")
        return redirect("accounts:bookings")
    
    if request.method == "POST":
        action = request.POST.get("action")  # accept or decline
        
        if action == "accept":
            booking.status = Booking.STATUS_ACCEPTED
            booking.instructor_response_date = timezone.now()
            booking.save()
            messages.success(request, f"Booking accepted for {booking.student.username}")
        elif action == "decline":
            decline_reason = request.POST.get("decline_reason", "")
            booking.status = Booking.STATUS_DECLINED
            booking.decline_reason = decline_reason
            booking.instructor_response_date = timezone.now()
            booking.save()
            messages.info(request, "Booking declined")
        
        return redirect("accounts:bookings")
    
    return render(request, "accounts/respond_booking.html", {
        "booking": booking,
        "page_title": "Respond to Booking"
    })


@login_required
def bookings_page(request):
    """View active bookings (pending/accepted) as seeker and as provider — UN-64"""
    ACTIVE = ("pending", "accepted")

    # Bookings this user made as a seeker — only active ones
    bookings_as_seeker = Booking.objects.filter(
        student=request.user,
        status__in=ACTIVE,
    ).select_related("skill_post", "skill_post__provider").order_by("-created_at")

    for booking in bookings_as_seeker:
        booking.can_rate = booking_can_be_rated(booking)

    # Bookings for skill posts this user provides — only active ones
    bookings_as_provider = Booking.objects.filter(
        skill_post__provider=request.user,
        status__in=ACTIVE,
    ).select_related("student", "skill_post").order_by("-created_at")

    context = {
        "bookings_as_seeker": bookings_as_seeker,
        "bookings_as_provider": bookings_as_provider,
        "page_title": "My Bookings",
        "active_page": "bookings",
    }
    return render(request, "accounts/bookings.html", context)



@login_required
def booking_detail(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permission
    if booking.student != request.user and booking.skill_post.provider != request.user:
        return HttpResponseForbidden("You cannot view this booking")
    
    return render(request, "accounts/booking_detail.html", {
        "booking": booking,
        "page_title": f"Booking Details: {booking.skill_post.title}"
    })


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking request"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only student can cancel
    if booking.student != request.user:
        return HttpResponseForbidden("You cannot cancel this booking")
    
    if booking.status in [Booking.STATUS_COMPLETED, Booking.STATUS_DECLINED]:
        messages.error(request, "Cannot cancel a completed or declined booking")
        return redirect("accounts:bookings")
    
    if request.method == "POST":
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.success(request, "Booking cancelled")
        return redirect("accounts:bookings")
    
    return render(request, "accounts/cancel_booking.html", {
        "booking": booking,
        "page_title": "Cancel Booking"
    })


@login_required
def mark_session_complete(request, booking_id):
    """Mark a session as completed and create session history (UN-64)"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only instructor can mark as complete
    if booking.skill_post.provider != request.user:
        return HttpResponseForbidden("Only instructor can mark session complete")
    
    if booking.status != Booking.STATUS_ACCEPTED:
        messages.error(request, "Only accepted bookings can be marked complete")
        return redirect("accounts:bookings")
    
    # Create session history record
    session = SessionHistory.objects.create(
        booking=booking,
        scheduled_date=booking.requested_date or timezone.now(),
        attendance_status=SessionHistory.ATTENDANCE_ATTENDED
    )
    
    booking.status = Booking.STATUS_COMPLETED
    booking.save()
    
    messages.success(request, "Session marked as completed!")
    return redirect("accounts:bookings")
