from django.contrib import admin
from .models import KnowledgeCategory, KnowledgeArticle, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'send_schedule', 'created_at')
    list_filter = ('category', 'is_published', 'send_schedule')
    search_fields = ('title', 'content', 'summary')
    inlines = [ImageInline]
    list_editable = ('is_published', 'send_schedule')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'caption', 'order', 'image')
    list_filter = ('article__category',)
    search_fields = ('caption', 'article__title')
