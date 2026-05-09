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
    
    # Skills - Browse & Detail
    path("skills.html", views.skills_page, name="skills_page"),
    path("skills/<int:post_id>/", views.skill_detail_page, name="skill_detail"),
    path("skill-detail.html", views.skills_page, name="skill_detail_legacy"),
    
    # Skills - UN-44: Create/Edit/Delete
    path("skill/create/", views.create_skill_post, name="create_skill_post"),
    path("skill/<int:post_id>/edit/", views.edit_skill_post, name="edit_skill_post"),
    path("skill/<int:post_id>/delete/", views.delete_skill_post, name="delete_skill_post"),
    
    # Moderation - UN-48
    path("moderation.html", views.moderation_dashboard, name="moderation"),
    path("moderation/<int:post_id>/", views.moderate_skill_post, name="moderate_skill_post"),
    
    # Bookings
    path("bookings.html", views.bookings_page, name="bookings"),
    
    # Alumni
    path("alumni.html", views.alumni_page, name="alumni"),
    
    # Profile
    path("profile.html", views.profile_page, name="profile"),
    
    # Rating
    path("rating.html", views.rating_page, name="rating"),
]
