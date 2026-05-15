from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_default_admin(sender, **kwargs):
    if getattr(sender, "name", None) != "accounts":
        return

    User = get_user_model()
    admin_user, _ = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@uniskills.local",
            "first_name": "System",
            "last_name": "Admin",
            "role": "student",
            "is_staff": True,
            "is_superuser": True,
            "is_email_verified": True,
            "is_alumni_verified": True,
        },
    )

    admin_user.email = "admin@uniskills.local"
    admin_user.first_name = "System"
    admin_user.last_name = "Admin"
    admin_user.role = "student"
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_email_verified = True
    admin_user.is_alumni_verified = True
    admin_user.set_password("admin")
    admin_user.save()