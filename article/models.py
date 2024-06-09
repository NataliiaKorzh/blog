from django.db import models

from user.models import User


class Article(models.Model):

    """
    Model representing an article.

    This model stores information about an article including its title, content,
    publication date, and author.

    Attributes:
        title (str): The title of the article.
        content (str): The content of the article.
        publication_date (DateTime): The date and time when the article was published.
        author (User): The user who authored the article.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
