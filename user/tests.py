from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

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
