from django.contrib import admin
from .models import NotificationLog

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'is_sent', 'sent_at', 'created_at', 'message_preview')
    list_filter = ('type', 'is_sent', 'created_at')
    search_fields = ('user__name', 'user__line_user_id', 'message')
    date_hierarchy = 'created_at'

    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'ข้อความ'
