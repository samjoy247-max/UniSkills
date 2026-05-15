from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from ..models import CustomUser, Rating


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "department",
            "university_id",
            "graduation_year",
            "major",
            "current_company",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs["placeholder"] = "Choose your display username"

        if self.user and self.user.role == "student":
            self.fields["graduation_year"].widget = forms.HiddenInput()
            self.fields["major"].widget = forms.HiddenInput()
            self.fields["current_company"].widget = forms.HiddenInput()
        else:
            self.fields["department"].widget = forms.HiddenInput()
            self.fields["university_id"].widget = forms.HiddenInput()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if self.user and self.user.role == "student" and not email.endswith("@uap-bd.edu"):
            raise ValidationError("Student email must be @uap-bd.edu")
        return email


@login_required
def profile_page(request):
    received_ratings = Rating.objects.filter(skill_post__provider=request.user).select_related(
        "rater", "skill_post"
    ).order_by("-created_at")
    rating_summary = received_ratings.aggregate(avg=Avg("rating"), total=Count("id"))
    avg_received_rating = round(rating_summary["avg"], 1) if rating_summary["avg"] else 0.0

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {
        "active_page": "profile",
        "form": form,
        "avg_received_rating": avg_received_rating,
        "received_rating_count": rating_summary["total"],
        "recent_received_ratings": received_ratings[:5],
    })


@login_required
def rating_page(request):
    return render(request, "accounts/rating.html", {"active_page": "rating"})
