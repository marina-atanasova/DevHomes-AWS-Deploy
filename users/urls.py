from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import dashboard, RegisterView, SimplePasswordResetView, ProfileEditView

urlpatterns = [
    path(
        "login/",auth_views.LoginView.as_view(template_name="users/login.html"),name="login",
    ),
    path(
        "logout/",auth_views.LogoutView.as_view(),name="logout",
    ),
    path("dashboard/", dashboard, name="dashboard"),
    path(
            "register/",RegisterView.as_view(),name="register",
        ),

    path("simple-reset-password/", SimplePasswordResetView.as_view(),name="simple_password_reset",),
    path("profile/edit/", ProfileEditView.as_view(), name="edit_profile"),
]