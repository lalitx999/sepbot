from django.urls import path
from .views import RegisterView, ProfileView
from .doctor_views import (
    doctor_login, doctor_logout, doctor_dashboard,
    doctor_vitals, doctor_screenings, doctor_daily_checks,
    doctor_families, doctor_users, doctor_knowledge,
    doctor_faq, doctor_notifications,
    api_patient_detail, api_update_patient_notes
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account-register'),
    path('profile/<str:line_user_id>/', ProfileView.as_view(), name='account-profile'),
    
    # Doctor Portal Endpoints
    path('doctor/login/', doctor_login, name='doctor-login'),
    path('doctor/logout/', doctor_logout, name='doctor-logout'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),
    path('doctor/vitals/', doctor_vitals, name='doctor-vitals'),
    path('doctor/screenings/', doctor_screenings, name='doctor-screenings'),
    path('doctor/daily-checks/', doctor_daily_checks, name='doctor-daily-checks'),
    path('doctor/families/', doctor_families, name='doctor-families'),
    path('doctor/users/', doctor_users, name='doctor-users'),
    path('doctor/knowledge/', doctor_knowledge, name='doctor-knowledge'),
    path('doctor/faq/', doctor_faq, name='doctor-faq'),
    path('doctor/notifications/', doctor_notifications, name='doctor-notifications'),

    # Doctor API Endpoints
    path('doctor/patient/<int:user_id>/', api_patient_detail, name='doctor-api-patient-detail'),
    path('doctor/patient/<int:user_id>/notes/', api_update_patient_notes, name='doctor-api-patient-notes'),
]


