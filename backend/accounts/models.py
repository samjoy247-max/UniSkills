from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("alumni", "Alumni"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    department = models.CharField(max_length=100, blank=True)
    university_id = models.CharField(max_length=50, blank=True)

    # Alumni onboarding fields
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=120, blank=True)

    is_alumni_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class SkillPost(models.Model):
    CATEGORY_TECHNICAL = "technical"
    CATEGORY_NON_TECHNICAL = "non_technical"
    CATEGORY_OTHER = "other"
    CATEGORY_CHOICES = [
        (CATEGORY_TECHNICAL, "Technical"),
        (CATEGORY_NON_TECHNICAL, "Non-Technical"),
        (CATEGORY_OTHER, "Other"),
    ]

    MODE_ONLINE = "online"
    MODE_OFFLINE = "offline"
    MODE_BOTH = "both"
    MODE_CHOICES = [
        (MODE_ONLINE, "Online"),
        (MODE_OFFLINE, "Offline"),
        (MODE_BOTH, "Both"),
    ]

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="skill_posts")
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    session_mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    available_time = models.DateTimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    rejection_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
