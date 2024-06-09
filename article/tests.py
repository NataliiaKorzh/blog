from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from article.models import Article
from article.serializers import ArticleSerializer

ARTICLE_URL = reverse("article:article_list")


def sample_article(**params):
    defaults = {
        "title": "Sample article",
        "content": "Sample content",
        "publication_date": "2024-06-03 14:00:00",
    }
    defaults.update(params)

    return Article.objects.create(**defaults)


def detail_url(article_id):
    return reverse("article:article_detail", args=[article_id])


class UnauthenticatedBlogApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(ARTICLE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBlogApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "password",
        )
        self.client.force_authenticate(self.user)

    def test_article_list(self) -> None:
        sample_article(author=self.user)
        sample_article(author=self.user)

        res = self.client.get(ARTICLE_URL)

        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_article(self) -> None:
        article = sample_article(author=self.user)

        url = detail_url(article.id)
        res = self.client.get(url)

        serializer = ArticleSerializer(article)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_article_forbidden_for_another_user(self) -> None:
        user2 = get_user_model().objects.create_user(
            "user2@test.com",
            "password2"
        )
        article = sample_article(author=user2)

        url = detail_url(article.id)
        res = self.client.get(url)

        serializer = ArticleSerializer(article)

        self.assertNotEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article(self) -> None:
        article = sample_article(author=self.user)
        article.title = "new title"
        article.content = "new content"
        article.save()

        url = detail_url(article.id)
        res = self.client.get(url)

        serializer = ArticleSerializer(article)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_article(self) -> None:
        article = sample_article(author=self.user)

        article.delete()

        article_id_1 = Article.objects.filter(id=1)

        self.assertEqual(article_id_1.count(), 0)
