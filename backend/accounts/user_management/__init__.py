from .admin_access import UniSkillsAuthenticationForm, dashboard, landing, login_user, logout_user
from .alumni import AlumniRegistrationForm, alumni_dashboard, alumni_page, register_alumni
from .profile import ProfileUpdateForm, profile_page, rating_page
from .student import (
    StudentRegistrationForm,
    SkillPostForm,
    bookings_page,
    create_skill_post,
    edit_skill_post,
    delete_skill_post,
    moderation_dashboard,
    moderate_skill_post,
    register_student,
    skill_detail_page,
    skills_page,
    student_dashboard,
)

__all__ = [
    "StudentRegistrationForm",
    "SkillPostForm",
    "AlumniRegistrationForm",
    "UniSkillsAuthenticationForm",
    "ProfileUpdateForm",
    "landing",
    "register_student",
    "register_alumni",
    "login_user",
    "logout_user",
    "dashboard",
    "student_dashboard",
    "alumni_dashboard",
    "skills_page",
    "skill_detail_page",
    "create_skill_post",
    "edit_skill_post",
    "delete_skill_post",
    "moderation_dashboard",
    "moderate_skill_post",
    "bookings_page",
    "alumni_page",
    "profile_page",
    "rating_page",
]
