from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden

from ..models import CustomUser, AlumniPost


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


class AlumniPostForm(forms.ModelForm):
    """Form for alumni to create/edit posts (UN-82)"""
    class Meta:
        model = AlumniPost
        fields = ["topic", "title", "content", "contact_link"]
        widgets = {
            "topic": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "contact_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://linkedin.com/in/yourprofile"}),
        }


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

    # Alumni sees their own posts
    my_posts = AlumniPost.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "accounts/alumni_dashboard.html", {
        "active_page": "alumni_dashboard",
        "my_posts": my_posts,
    })


@login_required
def alumni_page(request):
    """UN-81, UN-83: Browse verified alumni and their approved posts"""
    verified_alumni = CustomUser.objects.filter(
        role="alumni", is_alumni_verified=True
    ).order_by("username")

    approved_posts = AlumniPost.objects.filter(
        status=AlumniPost.STATUS_APPROVED
    ).select_related("author").order_by("-created_at")

    return render(request, "accounts/alumni.html", {
        "active_page": "alumni",
        "verified_alumni": verified_alumni,
        "alumni_posts": approved_posts,
    })


@login_required
def create_alumni_post(request):
    """UN-82: Alumni create a post"""
    if request.user.role != "alumni" or not request.user.is_alumni_verified:
        messages.error(request, "Only verified alumni can create posts.")
        return redirect("accounts:alumni_dashboard")

    if request.method == "POST":
        form = AlumniPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = AlumniPost.STATUS_PENDING
            post.save()
            messages.success(request, "Post submitted for admin approval.")
            return redirect("accounts:alumni_dashboard")
    else:
        form = AlumniPostForm()

    return render(request, "accounts/alumni_dashboard.html", {
        "form": form,
        "active_page": "alumni_dashboard",
        "show_post_form": True,
    })


@login_required
def delete_alumni_post(request, post_id):
    """UN-82: Alumni delete their own post"""
    post = get_object_or_404(AlumniPost, id=post_id)
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this post.")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("accounts:alumni_dashboard")


@login_required
def moderate_alumni_post(request, post_id):
    """UN-85, UN-86: Admin approve/reject alumni posts"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can moderate alumni posts.")

    post = get_object_or_404(AlumniPost, id=post_id)

    if request.method == "POST":
        action = request.POST.get("action")
        reason = request.POST.get("reason", "")
        if action == "approve":
            post.status = AlumniPost.STATUS_APPROVED
            messages.success(request, f"Alumni post '{post.title}' approved.")
        elif action == "reject":
            post.status = AlumniPost.STATUS_REJECTED
            post.rejection_reason = reason
            messages.warning(request, f"Alumni post '{post.title}' rejected.")
        post.save()
        return redirect("accounts:alumni_moderation")

    return render(request, "accounts/alumni_moderation_dashboard.html", {
        "post": post,
        "page_title": f"Moderate: {post.title}",
    })


@login_required
def alumni_moderation_dashboard(request):
    """UN-85: Admin dashboard for alumni post moderation"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can access this page.")

    pending_posts = AlumniPost.objects.filter(
        status=AlumniPost.STATUS_PENDING
    ).select_related("author").order_by("-created_at")

    return render(request, "accounts/alumni_moderation_dashboard.html", {
        "pending_posts": pending_posts,
        "page_title": "Alumni Post Moderation",
    })
