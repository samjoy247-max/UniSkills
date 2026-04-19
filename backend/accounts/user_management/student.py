from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from ..models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["username", "email", "department", "university_id", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "yourname@uap-bd.edu"
        self.fields["university_id"].widget.attrs["placeholder"] = "e.g. 23101084"
        self.fields["department"].widget.attrs["placeholder"] = "e.g. CSE"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if not email.endswith("@uap-bd.edu"):
            raise ValidationError("Student registration requires a valid @uap-bd.edu email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        user.is_alumni_verified = False
        if commit:
            user.save()
        return user


def register_student(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student registration successful. Please log in.")
            return redirect("accounts:login")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register_student.html", {"form": form})


@login_required
def student_dashboard(request):
    if request.user.role == "alumni" and not (request.user.is_staff or request.user.is_superuser):
        return redirect("accounts:alumni_dashboard")
    return render(request, "accounts/student_dashboard.html", {"active_page": "dashboard"})


@login_required
def skills_page(request):
    return render(request, "accounts/skills.html", {"active_page": "skills"})


@login_required
def bookings_page(request):
    return render(request, "accounts/bookings.html", {"active_page": "bookings"})
