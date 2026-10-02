from django.urls import path
from .views import (
    CategoryListView, ArticleListView, ArticleDetailView,
    web_article_list, web_article_detail
)

urlpatterns = [
    # REST API
    path('categories/', CategoryListView.as_view(), name='knowledge-categories'),
    path('articles/', ArticleListView.as_view(), name='knowledge-articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='knowledge-article-detail'),

    # Web Base HTML Views
    path('web/', web_article_list, name='knowledge-web-list'),
    path('web/<int:pk>/', web_article_detail, name='knowledge-web-detail'),
]
