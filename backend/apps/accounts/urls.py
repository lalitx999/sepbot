from django.urls import path
from .views import RegisterView, ProfileView
from .doctor_views import doctor_login, doctor_logout, doctor_dashboard, api_patient_detail, api_update_patient_notes

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account-register'),
    path('profile/<str:line_user_id>/', ProfileView.as_view(), name='account-profile'),
    
    # Doctor Portal Endpoints
    path('doctor/login/', doctor_login, name='doctor-login'),
    path('doctor/logout/', doctor_logout, name='doctor-logout'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),
    path('doctor/patient/<int:user_id>/', api_patient_detail, name='doctor-api-patient-detail'),
    path('doctor/patient/<int:user_id>/notes/', api_update_patient_notes, name='doctor-api-patient-notes'),
]

