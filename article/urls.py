from django.urls import path

from article.views import ArticleListView, ArticleDetailView, LatestArticleListView

urlpatterns = [
    path("/", ArticleListView.as_view(), name="article_list"),
    path("/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("/latest-articles/", LatestArticleListView.as_view(), name="latest_articles"),
]

app_name = "article"
