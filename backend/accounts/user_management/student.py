from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

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


class SkillPostForm(forms.ModelForm):
    class Meta:
        model = SkillPost
        fields = ["title", "description", "category", "session_mode", "available_time", "fee"]
        widgets = {
            "available_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_available_time(self):
        available_time = self.cleaned_data["available_time"]
        if available_time <= timezone.now():
            raise ValidationError("Available time must be in the future.")
        return available_time

    def clean_fee(self):
        fee = self.cleaned_data["fee"]
        if fee < 0:
            raise ValidationError("Fee cannot be negative.")
        return fee


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

    approved_posts = SkillPost.objects.select_related("provider").filter(status=SkillPost.STATUS_APPROVED)
    if query:
        approved_posts = approved_posts.filter(title__icontains=query)
    if category:
        approved_posts = approved_posts.filter(category=category)
    if mode:
        approved_posts = approved_posts.filter(session_mode=mode)

    form = None
    edit_post = None
    is_student = request.user.role == "student"
    my_posts = SkillPost.objects.none()

    if is_student:
        my_posts = SkillPost.objects.filter(provider=request.user)

        if request.method == "POST":
            post_id = request.POST.get("post_id")
            instance = None
            if post_id:
                instance = get_object_or_404(SkillPost, id=post_id, provider=request.user)

            form = SkillPostForm(request.POST, instance=instance)
            if form.is_valid():
                post = form.save(commit=False)
                post.provider = request.user
                # Editing re-enters moderation queue to keep content reviewed.
                post.status = SkillPost.STATUS_PENDING
                post.rejection_reason = ""
                post.save()
                if instance:
                    messages.success(request, "Skill post updated and sent for admin review.")
                else:
                    messages.success(request, "Skill post created and sent for admin review.")
                return redirect("accounts:skills")
            messages.error(request, "Please fix the errors in the form.")
        else:
            edit_id = request.GET.get("edit")
            if edit_id:
                edit_post = get_object_or_404(SkillPost, id=edit_id, provider=request.user)
                form = SkillPostForm(instance=edit_post)
            else:
                form = SkillPostForm()

    context = {
        "active_page": "skills",
        "skill_posts": approved_posts,
        "my_skill_posts": my_posts,
        "skill_form": form,
        "editing_post": edit_post,
        "search_query": query,
        "selected_category": category,
        "selected_mode": mode,
        "category_choices": SkillPost.CATEGORY_CHOICES,
        "mode_choices": SkillPost.MODE_CHOICES,
        "is_student_provider": is_student,
    }
    return render(request, "accounts/skills.html", context)


