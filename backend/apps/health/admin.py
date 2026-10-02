from django.contrib import admin
from .models import VitalSign

@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'temperature', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'respiratory_rate', 'spo2', 'recorded_at')
    list_filter = ('date', 'recorded_at')
    search_fields = ('user__name', 'user__id_card')
    date_hierarchy = 'date'
