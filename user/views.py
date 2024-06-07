from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, ProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):

    """
    API view for user registration.

    This view allows users to register by providing necessary information such as email and password.

    Attributes:
        queryset (QuerySet): The queryset representing all users.
        permission_classes (list): The list of permission classes allowing any user to register.
        serializer_class (Serializer): The serializer class for user registration.
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):

    """
    API view for user login.

    This view authenticates users and provides JWT tokens for authentication.

    Attributes:
        serializer_class (Serializer): The serializer class for user login.
    """

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ProfileView(generics.RetrieveUpdateAPIView):

    """
    API view for user profile.

    This view allows authenticated users to view and update their profile information.

    Attributes:
        queryset (QuerySet): The queryset representing all users.
        permission_classes (list): The list of permission classes allowing only authenticated users to access the view.
        serializer_class (Serializer): The serializer class for user profile.
    """

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    """
    API view for user logout.

    This view handles the blacklisting of the refresh token to log the user out.

    Attributes:
        permission_classes (list): The list of permission classes allowing only authenticated users to access the view.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except (TokenError, InvalidToken) as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
