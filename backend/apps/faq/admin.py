from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('order', 'question', 'category', 'answer_preview')
    list_display_links = ('question',)
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_editable = ('order', 'category')

    def answer_preview(self, obj):
        return obj.answer[:60] + "..." if len(obj.answer) > 60 else obj.answer
    answer_preview.short_description = 'ตัวอย่างคำตอบ'
