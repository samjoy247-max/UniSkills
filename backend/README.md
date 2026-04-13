# Backend (Django)

This folder is reserved for the Django implementation.

Suggested setup:

1. `python -m venv .venv`
2. Activate virtual environment
3. `pip install django`
4. `django-admin startproject uniskills_core .`
5. Create apps for accounts, skills, bookings, alumni, admin_moderation

Keep business rules aligned with SRS:

- Student module: seeker/provider flow
- Alumni module: profile + career posts
- Admin moderation required before public visibility
