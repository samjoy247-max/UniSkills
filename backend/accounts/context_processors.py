from .models import Booking


def booking_notifications(request):
    if not request.user.is_authenticated:
        return {
            "pending_booking_notifications": 0,
            "pending_provider_booking_count": 0,
            "pending_seeker_booking_count": 0,
        }

    # Requests waiting for this user to respond (as provider)
    pending_provider_booking_count = Booking.objects.filter(
        skill_post__provider=request.user,
        status=Booking.STATUS_PENDING,
    ).count()

    # Sessions accepted for this user (as seeker) — needs their attention
    pending_seeker_booking_count = Booking.objects.filter(
        student=request.user,
        status=Booking.STATUS_ACCEPTED,
    ).count()

    # Combined badge shown on EVERY page navbar
    total = pending_provider_booking_count + pending_seeker_booking_count

    return {
        "pending_booking_notifications": total,
        "pending_provider_booking_count": pending_provider_booking_count,
        "pending_seeker_booking_count": pending_seeker_booking_count,
    }