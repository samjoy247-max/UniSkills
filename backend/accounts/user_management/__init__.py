from .admin_access import UniSkillsAuthenticationForm, dashboard, landing, login_user, logout_user
from .alumni import AlumniRegistrationForm, alumni_dashboard, alumni_page, register_alumni
from .profile import ProfileUpdateForm, profile_page, rating_page, skill_detail_page
from .student import StudentRegistrationForm, bookings_page, register_student, skills_page, student_dashboard

__all__ = [
    "StudentRegistrationForm",
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
    "bookings_page",
    "alumni_page",
    "profile_page",
    "rating_page",
    "skill_detail_page",
]
