from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Avg

from .models import (
    CustomUser, SkillCategory, SkillModerationLog, SkillPost,
    SkillSearchFilter, SkillSlot, Booking, Rating, SessionHistory,
    AlumniPost, TimeBasedOTP,
)


# ==================== UN-88: User and Content Management ====================

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "role", "is_alumni_verified",
        "is_email_verified", "is_active", "is_staff",
    )
    list_filter = ("role", "is_alumni_verified", "is_active", "is_staff")
    search_fields = ("username", "email", "university_id", "major")
    # UN-89: Admin can toggle is_active to deactivate accounts
    list_editable = ("is_active",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "UniSkills Fields",
            {
                "fields": (
                    "role",
                    "department",
                    "university_id",
                    "graduation_year",
                    "major",
                    "current_company",
                    "is_alumni_verified",
                    "is_email_verified",
                    "profile_picture",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "UniSkills Fields",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "role",
                    "department",
                    "university_id",
                    "graduation_year",
                    "major",
                    "current_company",
                    "is_alumni_verified",
                ),
            },
        ),
    )

    # UN-79: Admin action to verify alumni accounts
    actions = ["verify_alumni", "deactivate_users"]

    def verify_alumni(self, request, queryset):
        updated = queryset.filter(role="alumni").update(is_alumni_verified=True)
        self.message_user(request, f"{updated} alumni account(s) verified.")
    verify_alumni.short_description = "Verify selected alumni accounts"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} account(s) deactivated.")
    deactivate_users.short_description = "Deactivate selected accounts"


@admin.register(SkillPost)
class SkillPostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "provider", "category", "session_mode",
        "fee", "status", "available_time", "created_at",
    )
    list_filter = ("status", "category", "session_mode")
    search_fields = ("title", "description", "provider__username", "provider__email")
    # UN-49: Admin can approve/reject from list view
    list_editable = ("status",)
    actions = ["approve_posts", "reject_posts", "delete_rejected_posts"]

    def approve_posts(self, request, queryset):
        updated = queryset.update(status=SkillPost.STATUS_APPROVED)
        self.message_user(request, f"{updated} skill post(s) approved.")
    approve_posts.short_description = "Approve selected skill posts"

    def reject_posts(self, request, queryset):
        updated = queryset.update(status=SkillPost.STATUS_REJECTED)
        self.message_user(request, f"{updated} skill post(s) rejected.")
    reject_posts.short_description = "Reject selected skill posts"

    def delete_rejected_posts(self, request, queryset):
        rejected_count = queryset.filter(status=SkillPost.STATUS_REJECTED).count()
        queryset.filter(status=SkillPost.STATUS_REJECTED).delete()
        self.message_user(request, f"{rejected_count} rejected skill post(s) deleted.")
    delete_rejected_posts.short_description = "Delete rejected skill posts"


# ==================== UN-88: Booking & Session Management ====================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "student", "skill_post", "status", "requested_date",
        "instructor_response_date", "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("student__username", "skill_post__title", "message")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SessionHistory)
class SessionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "booking", "scheduled_date", "attendance_status",
        "duration_minutes", "created_at",
    )
    list_filter = ("attendance_status", "scheduled_date")
    search_fields = ("booking__student__username", "booking__skill_post__title")
    readonly_fields = ("created_at", "updated_at")


# ==================== UN-73: Rating Management ====================

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("rater", "skill_post", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("rater__username", "skill_post__title", "review_text")
    readonly_fields = ("created_at", "updated_at")


# ==================== UN-85: Alumni Post Moderation ====================

@admin.register(AlumniPost)
class AlumniPostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "topic", "status", "created_at",
    )
    list_filter = ("status", "topic", "created_at")
    search_fields = ("title", "content", "author__username")
    # UN-86: Quick approval toggle from list view
    list_editable = ("status",)
    actions = ["approve_alumni_posts", "reject_alumni_posts", "delete_rejected_alumni_posts"]

    def approve_alumni_posts(self, request, queryset):
        updated = queryset.update(status=AlumniPost.STATUS_APPROVED)
        self.message_user(request, f"{updated} alumni post(s) approved.")
    approve_alumni_posts.short_description = "Approve selected alumni posts"

    def reject_alumni_posts(self, request, queryset):
        updated = queryset.update(status=AlumniPost.STATUS_REJECTED)
        self.message_user(request, f"{updated} alumni post(s) rejected.")
    reject_alumni_posts.short_description = "Reject selected alumni posts"

    def delete_rejected_alumni_posts(self, request, queryset):
        rejected_count = queryset.filter(status=AlumniPost.STATUS_REJECTED).count()
        queryset.filter(status=AlumniPost.STATUS_REJECTED).delete()
        self.message_user(request, f"{rejected_count} rejected alumni post(s) deleted.")
    delete_rejected_alumni_posts.short_description = "Delete rejected alumni posts"


# ==================== Auxiliary Models ====================

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(SkillModerationLog)
class SkillModerationLogAdmin(admin.ModelAdmin):
    list_display = ("skill_post", "moderator", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("skill_post__title", "moderator__username", "reason")
    readonly_fields = ("created_at",)


@admin.register(SkillSearchFilter)
class SkillSearchFilterAdmin(admin.ModelAdmin):
    list_display = ("filter_name", "user", "category", "session_mode", "is_favorite", "created_at")
    list_filter = ("category", "session_mode", "is_favorite", "created_at")
    search_fields = ("user__username", "filter_name", "keyword")


@admin.register(SkillSlot)
class SkillSlotAdmin(admin.ModelAdmin):
    list_display = ("skill_post", "start_time", "end_time", "max_students", "booked_students", "is_available")
    list_filter = ("is_available", "start_time")
    search_fields = ("skill_post__title",)
    readonly_fields = ("created_at",)


@admin.register(TimeBasedOTP)
class TimeBasedOTPAdmin(admin.ModelAdmin):
    list_display = ("user_email", "otp_code", "is_verified", "expires_at", "created_at")
    list_filter = ("is_verified",)
    search_fields = ("user_email",)
    readonly_fields = ("created_at",)


# ==================== UN-91: Basic Stats Admin Dashboard ====================

class UniSkillsAdminSite(admin.AdminSite):
    """Customized admin site with basic stats on the index page"""
    site_header = "UniSkills Administration"
    site_title = "UniSkills Admin"
    index_title = "Platform Management Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        # UN-92: total users
        extra_context["total_users"] = CustomUser.objects.filter(is_active=True).count()
        # UN-93: total approved skill posts
        extra_context["total_skill_posts"] = SkillPost.objects.filter(status=SkillPost.STATUS_APPROVED).count()
        # UN-94: total completed sessions
        extra_context["total_completed"] = Booking.objects.filter(status=Booking.STATUS_COMPLETED).count()
        # UN-95: verified alumni and published alumni posts
        extra_context["total_verified_alumni"] = CustomUser.objects.filter(
            role="alumni", is_alumni_verified=True
        ).count()
        extra_context["total_alumni_posts"] = AlumniPost.objects.filter(
            status=AlumniPost.STATUS_APPROVED
        ).count()
        # Pending items needing action
        extra_context["pending_skill_posts"] = SkillPost.objects.filter(status=SkillPost.STATUS_PENDING).count()
        extra_context["pending_alumni_posts"] = AlumniPost.objects.filter(status=AlumniPost.STATUS_PENDING).count()
        extra_context["pending_alumni_verif"] = CustomUser.objects.filter(
            role="alumni", is_alumni_verified=False, is_active=True
        ).count()
        return super().index(request, extra_context=extra_context)
