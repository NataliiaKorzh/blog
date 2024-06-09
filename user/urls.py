from django.urls import path, include
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterView, ProfileView, LogoutView

app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password_reset/",
        reset_password_request_token,
        name="password_reset_request"
    ),
    path(
        "password_reset_confirm/",
        reset_password_confirm,
        name="password_reset_confirm"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
