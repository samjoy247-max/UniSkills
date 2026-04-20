from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("index.html", views.landing, name="landing_html"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/alumni/", views.register_alumni, name="register_alumni"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard.html", views.student_dashboard, name="student_dashboard"),
    path("alumni-dashboard.html", views.alumni_dashboard, name="alumni_dashboard"),
    path("skills.html", views.skills_page, name="skills"),
    path("bookings.html", views.bookings_page, name="bookings"),
    path("alumni.html", views.alumni_page, name="alumni"),
    path("profile.html", views.profile_page, name="profile"),
    path("rating.html", views.rating_page, name="rating"),
    path("skill-detail.html", views.skill_detail_page, name="skill_detail"),
]
