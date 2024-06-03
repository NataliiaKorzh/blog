from django.urls import path

from article.views import ArticleListView, ArticleDetailView


urlpatterns = [
    path('api/articles/', ArticleListView.as_view(), name="article_list"),
    path('api/articles/<int:pk>/', ArticleDetailView.as_view(), name="article_detail"),
]

app_name = "article"
