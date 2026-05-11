from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # Landing & Auth
    path("", views.landing, name="landing"),
    path("index.html", views.landing, name="landing_html"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/alumni/", views.register_alumni, name="register_alumni"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    # Dashboards
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard.html", views.student_dashboard, name="student_dashboard"),
    path("alumni-dashboard.html", views.alumni_dashboard, name="alumni_dashboard"),

    # Skills - Browse & Detail (UN-52, UN-56)
    path("skills.html", views.skills_page, name="skills_page"),
    path("skills/<int:post_id>/", views.skill_detail_page, name="skill_detail"),
    path("skill-detail.html", views.skills_page, name="skill_detail_legacy"),

    # Skills - CRUD (UN-44)
    path("skill/create/", views.create_skill_post, name="create_skill_post"),
    path("skill/<int:post_id>/edit/", views.edit_skill_post, name="edit_skill_post"),
    path("skill/<int:post_id>/delete/", views.delete_skill_post, name="delete_skill_post"),

    # Skill Post Moderation - UN-48
    path("moderation.html", views.moderation_dashboard, name="moderation_dashboard"),
    path("moderation/<int:post_id>/", views.moderate_skill_post, name="moderate_skill_post"),

    # Bookings - UN-60, UN-64
    path("bookings.html", views.bookings_page, name="bookings"),
    path("booking/create/<int:post_id>/", views.create_booking, name="create_booking"),
    path("booking/<int:booking_id>/", views.booking_detail, name="booking_detail"),
    path("booking/<int:booking_id>/respond/", views.respond_booking, name="respond_booking"),
    path("booking/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("booking/<int:booking_id>/complete/", views.mark_session_complete, name="mark_session_complete"),

    # Session History - UN-64
    path("sessions/", views.session_history, name="session_history"),

    # Alumni - UN-77, UN-81, UN-82, UN-85
    path("alumni.html", views.alumni_page, name="alumni"),
    path("alumni/post/create/", views.create_alumni_post, name="create_alumni_post"),
    path("alumni/post/<int:post_id>/delete/", views.delete_alumni_post, name="delete_alumni_post"),
    path("alumni/moderation/", views.alumni_moderation_dashboard, name="alumni_moderation"),
    path("alumni/moderation/<int:post_id>/", views.moderate_alumni_post, name="moderate_alumni_post"),

    # Profile - UN-36
    path("profile.html", views.profile_page, name="profile"),

    # Rating - UN-69, UN-73
    path("rating.html", views.rating_page, name="rating"),
    path("skill/<int:post_id>/rate/", views.submit_rating, name="submit_rating"),
]
