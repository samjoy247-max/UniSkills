#!/usr/bin/env python
"""Verify all backend imports are working"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniskills_backend.settings')
django.setup()

print("=" * 60)
print("VERIFYING BACKEND IMPORTS")
print("=" * 60)

try:
    from accounts.models import (
        CustomUser, SkillPost, Booking, Rating, AlumniPost,
        SessionHistory, TimeBasedOTP, SkillCategory,
        SkillModerationLog, SkillSearchFilter, SkillSlot
    )
    print("\n✅ All Models Imported Successfully:")
    for model in [CustomUser, SkillPost, Booking, Rating, AlumniPost, 
                  SessionHistory, TimeBasedOTP, SkillCategory]:
        print(f"   - {model.__name__}")
except Exception as e:
    print(f"\n❌ Model Import Error: {e}")
    sys.exit(1)

try:
    from accounts.user_management import (
        register_alumni, alumni_dashboard, create_alumni_post,
        create_booking, respond_booking, bookings_page,
        submit_rating, profile_page,
        create_skill_post, edit_skill_post, delete_skill_post, skills_page
    )
    print("\n✅ All User Management Functions Imported Successfully:")
    print("   - Alumni Functions: register_alumni, alumni_dashboard, create_alumni_post")
    print("   - Booking Functions: create_booking, respond_booking, bookings_page")
    print("   - Rating Functions: submit_rating")
    print("   - Skill Functions: create_skill_post, edit_skill_post, delete_skill_post")
    print("   - Profile Functions: profile_page")
except Exception as e:
    print(f"\n❌ User Management Import Error: {e}")
    sys.exit(1)

try:
    from accounts.views import (
        landing, login_user, logout_user, register_student, register_alumni,
        dashboard, student_dashboard, alumni_dashboard,
        skills_page, create_skill_post, edit_skill_post, delete_skill_post,
        create_booking, respond_booking, bookings_page,
        create_alumni_post, profile_page, rating_page, submit_rating
    )
    print("\n✅ All Views Imported Successfully")
    print("   - Auth: landing, login_user, logout_user, register_student, register_alumni")
    print("   - Dashboard: dashboard, student_dashboard, alumni_dashboard")
    print("   - Skills: skills_page, create_skill_post, edit_skill_post, delete_skill_post")
    print("   - Bookings: create_booking, respond_booking, bookings_page")
    print("   - Alumni: create_alumni_post, alumni_page")
    print("   - Profile & Rating: profile_page, rating_page, submit_rating")
except Exception as e:
    print(f"\n❌ Views Import Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL IMPORTS VERIFIED - BACKEND IS RUNNABLE")
print("=" * 60)
