from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, SkillPost


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
    search_fields = ("title", "provider__username", "provider__email")
