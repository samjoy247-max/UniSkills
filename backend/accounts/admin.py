from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, SkillCategory, SkillModerationLog, SkillPost, SkillSearchFilter, SkillSlot


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_alumni_verified",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "is_alumni_verified", "is_active", "is_staff")
    search_fields = ("username", "email", "university_id", "major")

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


@admin.register(SkillPost)
class SkillPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "provider",
        "category",
        "session_mode",
        "fee",
        "status",
        "available_time",
        "created_at",
    )
    list_filter = ("status", "category", "session_mode")
    search_fields = ("title", "description", "provider__username", "provider__email")


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
