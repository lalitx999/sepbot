from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import KnowledgeCategory, KnowledgeArticle
from .serializers import KnowledgeCategorySerializer, KnowledgeArticleSerializer

import re

def sort_by_chapter(articles_qs):
    def get_chap_num(article):
        match = re.search(r'บทที่\s*(\d+)', article.title)
        if match:
            return int(match.group(1))
        return 999
    return sorted(articles_qs, key=get_chap_num)


class CategoryListView(APIView):
    def get(self, request):
        categories = KnowledgeCategory.objects.all().order_by('order')
        return Response(KnowledgeCategorySerializer(categories, many=True).data)


class ArticleListView(APIView):
    def get(self, request):
        category_slug = request.query_params.get('category')
        articles = KnowledgeArticle.objects.filter(is_published=True)
        if category_slug:
            articles = articles.filter(category__slug=category_slug)
        sorted_articles = sort_by_chapter(articles)
        return Response(KnowledgeArticleSerializer(sorted_articles, many=True).data)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(KnowledgeArticle, pk=pk, is_published=True)
        return Response(KnowledgeArticleSerializer(article).data)


# Web Base HTML Views (For LIFF / In-app browser)
def web_article_list(request):
    categories = KnowledgeCategory.objects.all().order_by('order')
    category_slug = request.GET.get('category')
    articles = KnowledgeArticle.objects.filter(is_published=True)
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    sorted_articles = sort_by_chapter(articles)

    return render(request, 'knowledge/list.html', {
        'categories': categories,
        'articles': sorted_articles,
        'selected_category': category_slug,
    })

def web_article_detail(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk, is_published=True)
    return render(request, 'knowledge/detail.html', {
        'article': article,
        'images': article.images.all().order_by('order'),
    })
