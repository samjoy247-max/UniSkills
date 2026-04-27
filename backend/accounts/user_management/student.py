from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
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


class ModerationForm(forms.Form):
    ACTION_CHOICES = [
        ("approve", "Approve"),
        ("reject", "Reject"),
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect())
    rejection_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for rejection (required if rejecting)"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        reason = cleaned_data.get("rejection_reason", "").strip()

        if action == "reject" and not reason:
            raise ValidationError("Rejection reason is required when rejecting a post.")
        return cleaned_data


def get_skill_filter_inputs(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    mode = request.GET.get("mode", "").strip()
    return query, category, mode


def apply_keyword_filter(skill_posts, query):
    if query:
        skill_posts = skill_posts.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(provider__username__icontains=query)
        )
    return skill_posts


def apply_category_filter(skill_posts, category):
    if category:
        skill_posts = skill_posts.filter(category=category)
    return skill_posts


def apply_mode_filter(skill_posts, mode):
    if mode:
        skill_posts = skill_posts.filter(session_mode=mode)
    return skill_posts


def build_skill_filter_context(query, category, mode):
    return {
        "search_query": query,
        "selected_category": category,
        "selected_mode": mode,
        "category_choices": SkillPost.CATEGORY_CHOICES,
        "mode_choices": SkillPost.MODE_CHOICES,
    }


def get_approved_skill_feed():
    return SkillPost.objects.select_related("provider").filter(status=SkillPost.STATUS_APPROVED)


def hide_unavailable_skill_slots(skill_posts):
    return skill_posts.filter(available_time__gt=timezone.now())


def order_skill_feed(skill_posts):
    return skill_posts.order_by("available_time", "-created_at")


def get_browse_skill_feed():
    skill_posts = get_approved_skill_feed()
    skill_posts = hide_unavailable_skill_slots(skill_posts)
    skill_posts = order_skill_feed(skill_posts)
    return skill_posts


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
    query, category, mode = get_skill_filter_inputs(request)

    skill_posts = get_browse_skill_feed()
    skill_posts = apply_keyword_filter(skill_posts, query)
    skill_posts = apply_category_filter(skill_posts, category)
    skill_posts = apply_mode_filter(skill_posts, mode)

    form = None
    edit_post = None
    my_posts = SkillPost.objects.none()
    is_student = request.user.role == "student"

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
        "skill_posts": skill_posts,
        "my_skill_posts": my_posts,
        "skill_form": form,
        "editing_post": edit_post,
        "is_student_provider": is_student,
    }
    context.update(build_skill_filter_context(query, category, mode))
    return render(request, "accounts/skills.html", context)


@login_required
def delete_skill_post(request, post_id):
    if request.method != "POST":
        return redirect("accounts:skills")

    post = get_object_or_404(SkillPost, id=post_id, provider=request.user)
    post.delete()
    messages.success(request, "Skill post deleted.")
    return redirect("accounts:skills")


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


@login_required
def moderation_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("accounts:skills")

    pending_posts = SkillPost.objects.select_related("provider").filter(
        status=SkillPost.STATUS_PENDING
    ).order_by("-created_at")

    context = {
        "active_page": "moderation",
        "pending_posts": pending_posts,
    }
    return render(request, "accounts/moderation.html", context)


@login_required
def moderate_skill_post(request, post_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("accounts:skills")

    post = get_object_or_404(SkillPost, id=post_id, status=SkillPost.STATUS_PENDING)

    if request.method == "POST":
        form = ModerationForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data["action"]
            if action == "approve":
                post.status = SkillPost.STATUS_APPROVED
                post.rejection_reason = ""
                post.save()
                messages.success(request, f"Post '{post.title}' approved successfully.")
            elif action == "reject":
                reason = form.cleaned_data["rejection_reason"].strip()
                post.status = SkillPost.STATUS_REJECTED
                post.rejection_reason = reason
                post.save()
                messages.success(request, f"Post '{post.title}' rejected with reason provided.")
            return redirect("accounts:moderation")
        messages.error(request, "Please fix the errors in the form.")
    else:
        form = ModerationForm()

    context = {
        "active_page": "moderation",
        "post": post,
        "form": form,
    }
    return render(request, "accounts/moderate_post.html", context)
