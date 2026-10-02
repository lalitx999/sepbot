from rest_framework import serializers
from .models import KnowledgeCategory, KnowledgeArticle, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'caption', 'order']


class KnowledgeArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = KnowledgeArticle
        fields = ['id', 'category', 'category_name', 'title', 'content', 'summary', 'is_published', 'send_schedule', 'images', 'created_at']


class KnowledgeCategorySerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(source='articles.count', read_only=True)

    class Meta:
        model = KnowledgeCategory
        fields = ['id', 'name', 'slug', 'icon', 'order', 'articles_count']
