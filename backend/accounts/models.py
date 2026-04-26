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


