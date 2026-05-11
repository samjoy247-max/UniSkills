from .admin_access import UniSkillsAuthenticationForm, dashboard, landing, login_user, logout_user
from .alumni import (
    AlumniRegistrationForm,
    AlumniPostForm,
    alumni_dashboard,
    alumni_page,
    create_alumni_post,
    delete_alumni_post,
    moderate_alumni_post,
    alumni_moderation_dashboard,
    register_alumni,
)
from .profile import ProfileUpdateForm, profile_page, rating_page
from .student import (
    StudentRegistrationForm,
    SkillPostForm,
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
from .booking import (
    BookingForm,
    BookingDecisionForm,
    create_booking,
    respond_booking,
    bookings_page,
    booking_detail,
    cancel_booking,
    mark_session_complete,
)
from .otp_verification import verify_email_otp, resend_otp
from .rating import submit_rating

__all__ = [
    # Forms
    "StudentRegistrationForm",
    "SkillPostForm",
    "BookingForm",
    "BookingDecisionForm",
    "AlumniRegistrationForm",
    "AlumniPostForm",
    "UniSkillsAuthenticationForm",
    "ProfileUpdateForm",
    # Auth & core
    "landing",
    "register_student",
    "register_alumni",
    "login_user",
    "logout_user",
    "verify_email_otp",
    "resend_otp",
    "dashboard",
    # Student
    "student_dashboard",
    "skills_page",
    "skill_detail_page",
    "create_skill_post",
    "edit_skill_post",
    "delete_skill_post",
    "moderation_dashboard",
    "moderate_skill_post",
    # Booking
    "create_booking",
    "respond_booking",
    "bookings_page",
    "booking_detail",
    "cancel_booking",
    "mark_session_complete",
    # Alumni
    "alumni_dashboard",
    "alumni_page",
    "create_alumni_post",
    "delete_alumni_post",
    "moderate_alumni_post",
    "alumni_moderation_dashboard",
    # Profile & rating
    "profile_page",
    "rating_page",
    "submit_rating",
]
