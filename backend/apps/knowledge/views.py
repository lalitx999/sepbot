import os
import re
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import KnowledgeCategory, KnowledgeArticle
from .serializers import KnowledgeCategorySerializer, KnowledgeArticleSerializer

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


def ebook_viewer(request):
    """
    Interactive Page-Flip E-Book Reader for 10Oct.Ebook
    """
    ebook_dir = os.path.join(settings.MEDIA_ROOT, 'ebook_10oct')
    pages = []
    if os.path.exists(ebook_dir):
        files = os.listdir(ebook_dir)
        def sort_key(name):
            if name == 'Cover.png': return (0, 0)
            if name == 'คำนำ.png': return (0, 1)
            if name == 'สารบัญ.png': return (0, 2)
            m = re.match(r'^(\d+)\.png$', name)
            if m:
                return (1, int(m.group(1)))
            return (2, name)

        sorted_files = sorted([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=sort_key)
        for idx, f in enumerate(sorted_files, 1):
            title = f
            if f == 'Cover.png':
                title = 'หน้าปก'
            elif f == 'คำนำ.png':
                title = 'คำนำ'
            elif f == 'สารบัญ.png':
                title = 'สารบัญ'
            else:
                num = f.split('.')[0]
                title = f'หน้าที่ {num}'

            pages.append({
                'index': idx,
                'filename': f,
                'title': title,
                'url': f"/{settings.MEDIA_URL.strip('/')}/ebook_10oct/{f}"
            })

    # Table of contents bookmarks for quick jumping
    bookmarks = [
        {'title': 'หน้าปก', 'page': 1},
        {'title': 'คำนำ', 'page': 2},
        {'title': 'สารบัญ', 'page': 3},
        {'title': 'บทที่ 1: ความรู้พื้นฐานเกี่ยวกับภาวะเซพซิส', 'page': 4},
        {'title': 'บทที่ 2: การฟื้นตัวหลังภาวะเซพซิส (PSS)', 'page': 8},
        {'title': 'บทที่ 3: การสังเกตอาการและเฝ้าระวัง', 'page': 9},
        {'title': 'บทที่ 4: การดูแลแผลและการใช้สายสวน', 'page': 12},
        {'title': 'บทที่ 5: การใช้ยาอย่างถูกต้อง', 'page': 18},
        {'title': 'บทที่ 6: การป้องกันการติดเชื้อซ้ำ', 'page': 21},
        {'title': 'บทที่ 7: โภชนาการและการฟื้นฟูร่างกาย', 'page': 26},
        {'title': 'บทที่ 8: ติดต่อฉุกเฉินและคู่มือเพิ่มเติม', 'page': 38},
    ]

    return render(request, 'knowledge/ebook.html', {
        'pages': pages,
        'total_pages': len(pages),
        'bookmarks': bookmarks,
    })
