from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import post_password_reset
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.signals import password_reset_token_created

CREATE_USER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token_obtain_pair")
ME_URL = reverse("user:profile")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self) -> None:
        payload = {
            "name": "Test User",
            "email": "test@test.com",
            "password": "testpass",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)


class PrivateUserApiTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()

    def test_obtain_token_with_valid_credentials(self) -> None:
        payload = {
            "email": self.user.email,
            "password": "testpass",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_obtain_token_with_invalid_credentials(self) -> None:
        payload = {
            "email": self.user.email,
            "password": "wrong",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_authenticated(self) -> None:
        self.client.force_authenticate(user=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PasswordResetTokenCreatedTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="password"
        )

        self.factory = RequestFactory()
        self.request = self.factory.get(reverse("user:password_reset_request"))
        self.request.user = self.user
        self.reset_password_token = ResetPasswordToken.objects.create(user=self.user)

    def test_password_reset_email_sent(self):

        reset_password_token = ResetPasswordToken.objects.create(user=self.user)

        mock_instance = Mock()
        mock_instance.request = self.request

        password_reset_token_created(
            sender=ResetPasswordToken,
            instance=mock_instance,
            reset_password_token=reset_password_token,
        )

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(
            mail.outbox[0].subject, "Password Reset for Some Website Title"
        )

        self.assertEqual(mail.outbox[0].to, [self.user.email])

    def test_token_deleted_after_password_reset(self):

        post_password_reset.send(
            sender=ResetPasswordToken, instance=self.reset_password_token
        )

        with self.assertRaises(ResetPasswordToken.DoesNotExist):
            ResetPasswordToken.objects.get(key=self.reset_password_token.key)
