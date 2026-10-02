from django.urls import path
from .views import DailyCheckView, SepsisScreeningView

urlpatterns = [
    path('daily-check/', DailyCheckView.as_view(), name='assessment-daily-check'),
    path('screening/', SepsisScreeningView.as_view(), name='assessment-screening'),
]
