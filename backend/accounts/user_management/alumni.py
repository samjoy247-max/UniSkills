from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from ..models import CustomUser


class AlumniRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "graduation_year",
            "major",
            "current_company",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["current_company"].widget.attrs["placeholder"] = "e.g. Software Engineer @ Company"
        self.fields["major"].widget.attrs["placeholder"] = "e.g. CSE"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "alumni"
        user.is_alumni_verified = False
        if commit:
            user.save()
        return user


def register_alumni(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumni registration submitted. Wait for admin verification before login.")
            return redirect("accounts:login")
    else:
        form = AlumniRegistrationForm()

    return render(request, "accounts/register_alumni.html", {"form": form})


@login_required
def alumni_dashboard(request):
    if request.user.role != "alumni" and not (request.user.is_staff or request.user.is_superuser):
        return redirect("accounts:student_dashboard")
    return render(request, "accounts/alumni_dashboard.html", {"active_page": "alumni_dashboard"})


@login_required
def alumni_page(request):
    return render(request, "accounts/alumni.html", {"active_page": "alumni"})
