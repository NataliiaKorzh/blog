from rest_framework import serializers

from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    """
    Serializer for the Article model.

    This serializer is used to serialize/deserialize Article objects to/from JSON format.

    """

    class Meta:
        model = Article
        fields = ["id", "title", "content", "publication_date", "author"]
        read_only_fields = ["author", "publication_date"]
