from django.contrib import admin
from .models import DailyCheck, SepsisScreening

@admin.register(DailyCheck)
class DailyCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'result_level', 'has_fever', 'has_wound', 'has_breathless', 'has_confused', 'has_less_eat', 'responder', 'responded_at')
    list_filter = ('result_level', 'responder', 'date')
    search_fields = ('user__name', 'user__id_card', 'user__line_user_id')
    date_hierarchy = 'date'


@admin.register(SepsisScreening)
class SepsisScreeningAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'has_red_flag', 'has_amber_flag', 'result')
    list_filter = ('has_red_flag', 'has_amber_flag', 'date')
    search_fields = ('user__name', 'user__id_card', 'result')
    date_hierarchy = 'date'
