from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden

from ..models import CustomUser, SkillPost
from ..otp_utils import create_and_send_otp


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
    """Form for creating/editing skill posts"""
    
    category = forms.ChoiceField(
        choices=SkillPost.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select skill category"
    )
    
    session_mode = forms.ChoiceField(
        choices=SkillPost.MODE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="How will you conduct the session?"
    )
    
    available_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        help_text="When is your skill session available?"
    )
    
    fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '500.00'}),
        help_text="Session fee in Taka (BDT)"
    )
    
    class Meta:
        model = SkillPost
        fields = ['title', 'description', 'category', 'session_mode', 'available_time', 'fee']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Advanced Django Development'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your skill in detail...'
            }),
        }
    
    def clean_available_time(self):
        from datetime import datetime
        available_time = self.cleaned_data.get('available_time')
        if available_time and available_time < datetime.now():
            raise ValidationError("Available time must be in the future")
        return available_time
    
    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee and fee < 0:
            raise ValidationError("Fee cannot be negative")
        return fee


def register_student(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Send OTP email
            create_and_send_otp(new_user.email)
            messages.success(request, "Student registration successful! OTP sent to your email. Please log in.")
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
    """Browse all approved skill posts with filtering"""
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
    """Show individual skill post details"""
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




# ==================== UN-44: SKILL POST CRUD ====================

@login_required
def create_skill_post(request):
    """Create a new skill post"""
    if request.method == "POST":
        form = SkillPostForm(request.POST)
        if form.is_valid():
            skill_post = form.save(commit=False)
            skill_post.provider = request.user
            skill_post.status = SkillPost.STATUS_PENDING  # Pending moderation
            skill_post.save()
            messages.success(request, "Skill post created! Waiting for moderation approval.")
            return redirect("accounts:skills_page")
    else:
        form = SkillPostForm()
    
    return render(request, "accounts/create_skill_post.html", {
        "form": form,
        "page_title": "Post a New Skill"
    })


@login_required
def edit_skill_post(request, post_id):
    """Edit an existing skill post"""
    skill_post = get_object_or_404(SkillPost, id=post_id)
    
    # Only provider or admin can edit
    if request.user != skill_post.provider and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this post")
    
    if request.method == "POST":
        form = SkillPostForm(request.POST, instance=skill_post)
        if form.is_valid():
            skill_post = form.save(commit=False)
            skill_post.status = SkillPost.STATUS_PENDING  # Reset to pending for re-review
            skill_post.save()
            messages.success(request, "Skill post updated! Resubmitted for moderation.")
            return redirect("accounts:skills_page")
    else:
        form = SkillPostForm(instance=skill_post)
    
    return render(request, "accounts/edit_skill_post.html", {
        "form": form,
        "skill_post": skill_post,
        "page_title": f"Edit: {skill_post.title}"
    })


@login_required
def delete_skill_post(request, post_id):
    """Delete a skill post with confirmation"""
    skill_post = get_object_or_404(SkillPost, id=post_id)
    
    # Only provider or admin can delete
    if request.user != skill_post.provider and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this post")
    
    if request.method == "POST":
        skill_post.delete()
        messages.success(request, "Skill post deleted successfully")
        return redirect("accounts:skills_page")
    
    return render(request, "accounts/delete_skill_post_confirm.html", {
        "skill_post": skill_post,
        "page_title": "Confirm Delete"
    })


# ==================== MODERATION ====================

@login_required
def moderation_dashboard(request):
    """Admin moderation dashboard for skill posts"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can access moderation")
    
    pending_posts = SkillPost.objects.filter(status=SkillPost.STATUS_PENDING).select_related("provider")
    
    return render(request, "accounts/moderation_dashboard.html", {
        "pending_posts": pending_posts,
        "page_title": "Skill Post Moderation"
    })


@login_required
def moderate_skill_post(request, post_id):
    """Approve or reject a skill post"""
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can moderate")
    
    skill_post = get_object_or_404(SkillPost, id=post_id)
    
    if request.method == "POST":
        action = request.POST.get("action")  # approve or reject
        reason = request.POST.get("reason", "")
        
        if action == "approve":
            skill_post.status = SkillPost.STATUS_APPROVED
            messages.success(request, f"Skill post '{skill_post.title}' approved!")
        elif action == "reject":
            skill_post.status = SkillPost.STATUS_REJECTED
            skill_post.rejection_reason = reason
            messages.warning(request, f"Skill post '{skill_post.title}' rejected.")
        
        skill_post.save()
        return redirect("accounts:moderation_dashboard")
    
    return render(request, "accounts/moderate_skill_post.html", {
        "skill_post": skill_post,
        "page_title": f"Moderate: {skill_post.title}"
    })
