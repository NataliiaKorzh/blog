from django.urls import path, include
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
        r"password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
