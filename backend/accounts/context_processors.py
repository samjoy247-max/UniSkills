from .models import Booking


def booking_notifications(request):
    if not request.user.is_authenticated:
        return {
            "pending_booking_notifications": 0,
            "pending_provider_booking_count": 0,
            "pending_seeker_booking_count": 0,
        }

    pending_provider_booking_count = Booking.objects.filter(
        skill_post__provider=request.user,
        status=Booking.STATUS_PENDING,
    ).count()

    pending_seeker_booking_count = Booking.objects.filter(
        student=request.user,
        status__in=[Booking.STATUS_ACCEPTED, Booking.STATUS_COMPLETED],
    ).count()

    return {
        "pending_booking_notifications": pending_provider_booking_count,
        "pending_provider_booking_count": pending_provider_booking_count,
        "pending_seeker_booking_count": pending_seeker_booking_count,
    }