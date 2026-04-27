from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render


class UniSkillsAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        identifier = self.data.get("username", "").strip()
        if "@" in identifier:
            user = (
                get_user_model()
                .objects.filter(email__iexact=identifier)
                .order_by("-is_active", "id")
                .first()
            )
            if user:
                mutable_data = self.data.copy()
                mutable_data["username"] = user.get_username()
                self.data = mutable_data
        return super().clean()


def _post_login_destination(user):
    if user.is_staff or user.is_superuser:
        return "/admin/"
    if user.role == "alumni":
        return "accounts:alumni_dashboard"
    return "accounts:student_dashboard"


def landing(request):
    return render(request, "accounts/landing.html")


def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Keep student/alumni login isolated from admin sessions.
            logout(request)
            messages.info(request, "Student/Alumni login only. Admin login via /admin/.")
            return redirect("accounts:login")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = UniSkillsAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.error(request, "This account is deactivated. Contact admin.")
                return redirect("accounts:login")

            if user.is_staff or user.is_superuser:
                messages.error(request, "Admin login is allowed only at /admin/.")
                return redirect("accounts:login")

            if user.role == "alumni" and not user.is_alumni_verified:
                messages.error(request, "Alumni account pending verification by admin.")
                return redirect("accounts:login")

            login(request, user)
            return redirect(_post_login_destination(user))
    else:
        form = UniSkillsAuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("accounts:landing")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    return redirect(_post_login_destination(request.user))
