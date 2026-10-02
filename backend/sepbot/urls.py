from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from linebot.liff_views import liff_register, liff_select_type, liff_daily_check, liff_screening, liff_vitals
from accounts.doctor_views import doctor_login, doctor_logout, doctor_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/assessment/', include('assessment.urls')),
    path('api/v1/health/', include('health.urls')),
    path('api/v1/knowledge/', include('knowledge.urls')),
    path('api/v1/faq/', include('faq.urls')),
    path('api/v1/line/', include('linebot.urls')),

    # Doctor Portal Direct Views
    path('doctor/login/', doctor_login, name='doctor-login'),
    path('doctor/logout/', doctor_logout, name='doctor-logout'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor-dashboard'),

    # LIFF Web Page Views
    path('liff/register/', liff_register, name='liff-register'),
    path('liff/select-type/', liff_select_type, name='liff-select-type'),
    path('liff/daily-check/', liff_daily_check, name='liff-daily-check'),
    path('liff/screening/', liff_screening, name='liff-screening'),
    path('liff/vitals/', liff_vitals, name='liff-vitals'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

