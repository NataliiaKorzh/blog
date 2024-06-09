from rest_framework import generics, permissions

from article.models import Article
from article.serializers import ArticleSerializer


class ArticleListView(generics.ListCreateAPIView):
    """
    API view for listing and creating articles.

    This view allows authenticated users to list and create articles.

    Attributes:
        serializer_class (Serializer): The serializer class for article objects.
        permission_classes (list): The list of permission classes allowing only authenticated users to access the view.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get queryset for listing articles.

        Returns:
            QuerySet: The queryset of articles authored by the current user.
        """
        return self.request.user.articles.all()

    def perform_create(self, serializer):
        """
        Perform article creation.

        Args:
            serializer (Serializer): The serializer instance for article creation.
        """
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting articles.

    This view allows authenticated users to retrieve, update, and delete their own articles.

    Attributes:
        serializer_class (Serializer): The serializer class for article objects.
        permission_classes (list): The list of permission classes allowing only authenticated users to access the view.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get queryset for retrieving articles.

        Returns:
            QuerySet: The queryset of articles authored by the current user.
        """
        return Article.objects.filter(author=self.request.user)


class LatestArticleListView(generics.ListAPIView):
    """
    API view for listing the latest article.

    This view allows all users to retrieve the latest article.

    Attributes:
        queryset (QuerySet): The queryset for retrieving the latest article.
        serializer_class (Serializer): The serializer class for article objects.
    """
    queryset = Article.objects.order_by("-publication_date").first()
    serializer_class = ArticleSerializer
