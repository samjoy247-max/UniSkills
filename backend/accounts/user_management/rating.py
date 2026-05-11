"""
UN-73: Submit Rating/Review after a completed session
UN-69: View ratings is handled in student.py (skill_detail_page)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import Booking, Rating, SkillPost


@login_required
def submit_rating(request, post_id):
    """
    UN-73: Student submits a rating and review for a completed skill session.
    Only students who have a completed booking for this skill can rate it.
    Each student can only rate a skill once (unique_together on Rating model).
    """
    skill_post = get_object_or_404(SkillPost, id=post_id)

    # Check: student must have a completed booking for this skill
    completed_booking = Booking.objects.filter(
        student=request.user,
        skill_post=skill_post,
        status=Booking.STATUS_COMPLETED,
    ).first()

    if not completed_booking:
        messages.error(request, "You can only rate a skill after completing a session.")
        return redirect("accounts:skill_detail", post_id=post_id)

    # Check: has the student already rated this skill?
    already_rated = Rating.objects.filter(
        rater=request.user,
        skill_post=skill_post
    ).exists()

    if already_rated:
        messages.info(request, "You have already rated this skill.")
        return redirect("accounts:skill_detail", post_id=post_id)

    if request.method == "POST":
        rating_value_str = request.POST.get("rating", "")
        review_text = request.POST.get("review_text", "").strip()

        # Validate rating value
        valid_ratings = [1.0, 2.0, 3.0, 4.0, 5.0]
        try:
            rating_value = float(rating_value_str)
            if rating_value not in valid_ratings:
                raise ValueError()
        except (ValueError, TypeError):
            messages.error(request, "Please select a valid rating (1 to 5 stars).")
            return render(request, "accounts/rating_form.html", {
                "skill_post": skill_post,
                "booking": completed_booking,
            })

        # Get session record if available
        session = getattr(completed_booking, 'session', None)

        # Save the rating
        Rating.objects.create(
            rater=request.user,
            skill_post=skill_post,
            session=session,
            rating=rating_value,
            review_text=review_text,
        )

        messages.success(request, f"Thank you! Your {int(rating_value)}-star rating has been submitted.")
        return redirect("accounts:skill_detail", post_id=post_id)

    # GET: show the rating form
    return render(request, "accounts/rating_form.html", {
        "skill_post": skill_post,
        "booking": completed_booking,
        "page_title": f"Rate: {skill_post.title}",
    })
