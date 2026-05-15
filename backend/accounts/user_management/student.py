from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden

from ..models import CustomUser, SkillPost, Booking, AlumniPost, Rating
from ..otp_utils import create_and_send_otp
from django.db.models import Avg


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
        from django.utils import timezone
        available_time = self.cleaned_data.get('available_time')
        if available_time and available_time < timezone.now():
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
            # Send OTP email and capture delivery status.
            _, email_sent, email_error = create_and_send_otp(new_user.email)
            # Store email in session for OTP verification
            request.session['pending_verification_email'] = new_user.email

            if email_sent:
                messages.success(request, "Registration successful! Please verify your email with the OTP sent to your inbox.")
            else:
                if email_error and "Console backend is active" in email_error:
                    messages.info(
                        request,
                        "Registration successful! OTP was printed in the server console because the app is running in development mode."
                    )
                else:
                    messages.warning(
                        request,
                        f"Registration completed, but OTP email could not be delivered. Details: {email_error or 'unknown error'}. "
                        "Please check SMTP configuration and click Resend OTP."
                    )
                if email_error:
                    print(f"[OTP SEND ERROR] {email_error}", flush=True)

            return redirect("accounts:verify_email_otp")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register_student.html", {"form": form})


@login_required
def student_dashboard(request):
    if request.user.role == "alumni" and not (request.user.is_staff or request.user.is_superuser):
        return redirect("accounts:alumni_dashboard")
    
    # Get user's skill posts
    my_skill_posts = SkillPost.objects.filter(provider=request.user).order_by("-created_at")
    
    # Get user's bookings as seeker
    bookings_as_seeker = Booking.objects.filter(
        student=request.user
    ).select_related("skill_post", "skill_post__provider").order_by("-created_at")[:3]
    
    # Get skill posts created by user that are approved
    approved_posts = my_skill_posts.filter(status=SkillPost.STATUS_APPROVED)
    
    # Calculate stats
    total_skill_posts = my_skill_posts.count()
    total_bookings = Booking.objects.filter(student=request.user).count()
    completed_sessions = Booking.objects.filter(
        student=request.user,
        status=Booking.STATUS_COMPLETED
    ).count()
    
    # Calculate average rating from completed sessions
    avg_rating = 0.0
    if completed_sessions > 0:
        ratings = Rating.objects.filter(
            rater=request.user,
            session__booking__student=request.user
        ).aggregate(avg=Avg('rating'))
        avg_rating = round(ratings['avg'], 1) if ratings['avg'] else 0.0
    
    # Get alumni posts
    try:
        alumni_posts = AlumniPost.objects.filter(
            status='approved'
        ).select_related('author').order_by("-created_at")[:2]
    except:
        alumni_posts = []
    
    context = {
        "active_page": "dashboard",
        "total_skill_posts": total_skill_posts,
        "total_bookings": total_bookings,
        "completed_sessions": completed_sessions,
        "avg_rating": avg_rating,
        "my_skill_posts": my_skill_posts,
        "bookings_as_seeker": bookings_as_seeker,
        "alumni_posts": alumni_posts,
    }
    
    return render(request, "accounts/student_dashboard.html", context)


@login_required
def skills_page(request):
    """Browse all approved skill posts with filtering"""
    # Only allow students/providers, not admin/staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin users cannot post skills. Use the admin panel to manage posts.")
        return redirect("accounts:dashboard")
    
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    mode = request.GET.get("mode", "").strip()
    edit_post_id = request.GET.get("edit", "").strip()

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

    # Student can act as both seeker and provider.
    is_student_provider = request.user.role in ["student", "provider"]
    my_skill_posts = SkillPost.objects.filter(provider=request.user).order_by("-id")

    editing_post = None
    if edit_post_id:
        try:
            editing_post = SkillPost.objects.get(id=int(edit_post_id), provider=request.user)
        except (SkillPost.DoesNotExist, ValueError):
            editing_post = None

    if request.method == "POST" and is_student_provider:
        if editing_post:
            form = SkillPostForm(request.POST, instance=editing_post)
        else:
            form = SkillPostForm(request.POST)

        if form.is_valid():
            skill_post = form.save(commit=False)
            skill_post.provider = request.user
            skill_post.status = SkillPost.STATUS_PENDING
            skill_post.save()
            messages.success(request, "Skill post submitted for moderation.")
            return redirect("accounts:skills_page")
    else:
        form = SkillPostForm(instance=editing_post) if editing_post else SkillPostForm()

    context = {
        "active_page": "skills",
        "skill_posts": skill_posts,
        "my_skill_posts": my_skill_posts,
        "is_student_provider": is_student_provider,
        "editing_post": editing_post,
        "skill_form": form,
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
    # Only allow students, not admin/staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin users cannot create skill posts. Use the admin panel instead.")
        return redirect("accounts:dashboard")
    
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
