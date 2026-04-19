from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


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
