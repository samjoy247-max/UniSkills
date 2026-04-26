from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..models import CustomUser, SkillPost


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
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    mode = request.GET.get("mode", "").strip()

    skill_posts = SkillPost.objects.select_related("provider").filter(status=SkillPost.STATUS_APPROVED)

    if query:
        skill_posts = skill_posts.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(provider__username__icontains=query)
        )
    if category:
        skill_posts = skill_posts.filter(category=category)
    if mode:
        skill_posts = skill_posts.filter(session_mode=mode)

    context = {
        "active_page": "skills",
        "skill_posts": skill_posts,
        "search_query": query,
        "selected_category": category,
        "selected_mode": mode,
        "category_choices": SkillPost.CATEGORY_CHOICES,
        "mode_choices": SkillPost.MODE_CHOICES,
    }
    return render(request, "accounts/skills.html", context)


@login_required
def skill_detail_page(request, post_id):
    skill_post = get_object_or_404(
        SkillPost.objects.select_related("provider"),
        id=post_id,
        status=SkillPost.STATUS_APPROVED,
    )
    return render(
        request,
        "accounts/skill-detail.html",
        {
            "active_page": "skills",
            "skill_post": skill_post,
        },
    )


@login_required
def bookings_page(request):
    return render(request, "accounts/bookings.html", {"active_page": "bookings"})
