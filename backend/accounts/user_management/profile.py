from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from ..models import CustomUser


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
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"active_page": "profile", "form": form})


@login_required
def rating_page(request):
    return render(request, "accounts/rating.html", {"active_page": "rating"})


@login_required
def skill_detail_page(request):
    return render(request, "accounts/skill-detail.html", {"active_page": "skills"})
