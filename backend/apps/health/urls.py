from django.urls import path
from .views import VitalSignView

urlpatterns = [
    path('vitals/', VitalSignView.as_view(), name='health-vitals-create'),
    path('vitals/<str:line_user_id>/', VitalSignView.as_view(), name='health-vitals-list'),
]
