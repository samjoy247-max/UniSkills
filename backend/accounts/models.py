from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with student/alumni roles"""
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
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text="Upload your profile picture",
    )

    def __str__(self):
        return self.username


class SkillPost(models.Model):
    """Skill posts created by students (UN-44)"""
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


class SkillCategory(models.Model):
    """Predefined skill categories (UN-52)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SkillModerationLog(models.Model):
    """Tracks moderation actions on skill posts (UN-48)"""
    ACTION_APPROVE = "approve"
    ACTION_REJECT = "reject"
    ACTION_CHOICES = [
        (ACTION_APPROVE, "Approved"),
        (ACTION_REJECT, "Rejected"),
    ]

    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name="moderation_logs")
    moderator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="moderation_actions")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.skill_post.title} - {self.get_action_display()}"


class SkillSearchFilter(models.Model):
    """Saved search filters for users (UN-52)"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved_filters")
    filter_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, blank=True, choices=SkillPost.CATEGORY_CHOICES)
    session_mode = models.CharField(max_length=10, blank=True, choices=SkillPost.MODE_CHOICES)
    keyword = models.CharField(max_length=100, blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.filter_name}"


class SkillSlot(models.Model):
    """Available time slots for skill sessions (UN-56)"""
    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name="slots")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_students = models.PositiveIntegerField(default=1)
    booked_students = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.skill_post.title} - {self.start_time}"


class AlumniPost(models.Model):
    """Alumni posts for networking and mentorship (UN-81, UN-82, UN-85)"""
    TOPIC_CAREER = "career_advice"
    TOPIC_JOBS = "job_opportunity"
    TOPIC_INDUSTRY = "industry_insights"
    TOPIC_MENTORSHIP = "mentorship"
    TOPIC_CHOICES = [
        (TOPIC_CAREER, "Career Advice"),
        (TOPIC_JOBS, "Job Opportunity"),
        (TOPIC_INDUSTRY, "Industry Insights"),
        (TOPIC_MENTORSHIP, "Mentorship"),
    ]

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="alumni_posts")
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    title = models.CharField(max_length=150)
    content = models.TextField()
    contact_link = models.URLField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    rejection_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class TimeBasedOTP(models.Model):
    """OTP for email verification during registration"""
    user_email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"OTP for {self.user_email} - Verified: {self.is_verified}"


class Booking(models.Model):
    """Booking requests for skill sessions (UN-60)"""
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings_made")
    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    message = models.TextField(blank=True, help_text="Student's request message")
    requested_date = models.DateTimeField(null=True, blank=True)
    instructor_response_date = models.DateTimeField(null=True, blank=True)
    decline_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["student", "skill_post"]]

    def __str__(self):
        return f"Booking #{self.id}: {self.student.username} → {self.skill_post.title} ({self.get_status_display()})"


class SessionHistory(models.Model):
    """Session history and attendance tracking (UN-64)"""
    ATTENDANCE_ATTENDED = "attended"
    ATTENDANCE_NO_SHOW = "no_show"
    ATTENDANCE_CANCELLED = "cancelled"
    ATTENDANCE_CHOICES = [
        (ATTENDANCE_ATTENDED, "Attended"),
        (ATTENDANCE_NO_SHOW, "No Show"),
        (ATTENDANCE_CANCELLED, "Cancelled"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="session")
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    attendance_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return f"Session: {self.booking.student.username} - {self.booking.skill_post.title} on {self.scheduled_date}"


class Rating(models.Model):
    """Rating and reviews for skill sessions (UN-69, UN-73)"""
    RATING_CHOICES = [
        (1.0, "Poor"),
        (2.0, "Fair"),
        (3.0, "Good"),
        (4.0, "Very Good"),
        (5.0, "Excellent"),
    ]

    rater = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ratings_given")
    skill_post = models.ForeignKey(SkillPost, on_delete=models.CASCADE, related_name="ratings")
    session = models.OneToOneField(SessionHistory, on_delete=models.CASCADE, related_name="rating", null=True, blank=True)
    rating = models.FloatField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["rater", "skill_post"]]

    def __str__(self):
        return f"{self.rater.username} rated {self.skill_post.title}: {self.rating} stars"
