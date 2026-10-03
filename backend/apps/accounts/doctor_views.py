from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Max, Prefetch, Count
from django.utils import timezone
from datetime import timedelta
import json

from accounts.models import LineUser, FamilyGroup
from assessment.models import DailyCheck, SepsisScreening
from health.models import VitalSign
from knowledge.models import KnowledgeArticle
from faq.models import FAQ
from notification.models import NotificationLog

def doctor_login(request):
    """Render Doctor & Nurse Portal Login Page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('doctor-dashboard')
        
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'doctor')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            request.session['doctor_role'] = role
            return redirect('doctor-dashboard')
        else:
            error_message = "เลขประจำตัว/ชื่อผู้ใช้ หรือรหัสผ่านไม่ถูกต้อง หรือยังไม่ได้รับสิทธิ์เข้าใช้งานระบบแพทย์"
            
    return render(request, 'doctor/login.html', {'error_message': error_message})

def doctor_logout(request):
    """Logout Doctor"""
    logout(request)
    return redirect('doctor-login')

@login_required(login_url='doctor-login')
def doctor_dashboard(request):
    """Main Doctor Dashboard Page with Live Patient Triage Context Data"""
    today = timezone.now().date()
    
    patients = LineUser.objects.filter(role='patient', is_registered=True).select_related('family')
    today_checks = DailyCheck.objects.filter(date=today)
    red_today_count = today_checks.filter(result_level='red').count()
    yellow_today_count = today_checks.filter(result_level='yellow').count()
    green_today_count = today_checks.filter(result_level='green').count()
    
    checked_user_ids = today_checks.values_list('user_id', flat=True)
    overdue_patients = patients.exclude(id__in=checked_user_ids)
    overdue_count = overdue_patients.count()
    
    patient_list = []
    for p in patients:
        latest_check = DailyCheck.objects.filter(user=p).order_by('-responded_at').first()
        latest_screening = SepsisScreening.objects.filter(user=p).order_by('-date').first()
        latest_vitals = VitalSign.objects.filter(user=p).order_by('-recorded_at').first()
        caregivers = LineUser.objects.filter(family=p.family, role='caregiver') if p.family else []
        primary_caregiver = caregivers.first()
        
        status_code = 'green'
        status_label = 'ปกติ'
        priority = 4
        
        if latest_screening and latest_screening.has_red_flag:
            status_code = 'red'
            status_label = '🔴 วิกฤต (Red Flag)'
            priority = 1
        elif latest_check and latest_check.result_level == 'red':
            status_code = 'red'
            status_label = '🔴 อาการรุนแรง (Red)'
            priority = 1
        elif latest_screening and latest_screening.has_amber_flag:
            status_code = 'yellow'
            status_label = '🟡 เฝ้าระวัง (Amber)'
            priority = 2
        elif latest_check and latest_check.result_level == 'yellow':
            status_code = 'yellow'
            status_label = '🟡 เฝ้าระวัง (Yellow)'
            priority = 2
        elif not latest_check or latest_check.date < today:
            status_code = 'overdue'
            status_label = '⚠️ ขาดส่งประเมินวันนี้'
            priority = 3
        else:
            status_code = 'green'
            status_label = '🟢 ปกติ'
            priority = 4
            
        patient_list.append({
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'family_code': p.family.code if p.family else 'N/A',
            'phone': p.phone_number or 'ไม่ระบุ',
            'id_card': p.id_card,
            'underlying_disease': p.underlying_disease or '-',
            'status_code': status_code,
            'status_label': status_label,
            'priority': priority,
            'latest_check': latest_check,
            'latest_vitals': latest_vitals,
            'primary_caregiver': primary_caregiver,
        })
        
    patient_list.sort(key=lambda x: x['priority'])
    
    context = {
        'total_patients': patients.count(),
        'red_count': red_today_count,
        'yellow_count': yellow_today_count,
        'green_count': green_today_count,
        'overdue_count': overdue_count,
        'patient_list': patient_list,
    }
    return render(request, 'doctor/dashboard.html', context)

@login_required(login_url='doctor-login')
def doctor_vitals(request):
    """Vital Signs Tracker Management View"""
    vitals = VitalSign.objects.select_related('user', 'family').order_by('-date', '-recorded_at')
    return render(request, 'doctor/vitals.html', {'vitals': vitals})

@login_required(login_url='doctor-login')
def doctor_screenings(request):
    """Sepsis Screening Management View"""
    screenings = SepsisScreening.objects.select_related('user', 'family').order_by('-date')
    return render(request, 'doctor/screenings.html', {'screenings': screenings})

@login_required(login_url='doctor-login')
def doctor_daily_checks(request):
    """Daily Symptom Checks Log View"""
    checks = DailyCheck.objects.select_related('user', 'family').order_by('-date', '-responded_at')
    return render(request, 'doctor/daily_checks.html', {'checks': checks})

@login_required(login_url='doctor-login')
def doctor_families(request):
    """Family Groups Management View"""
    families = FamilyGroup.objects.annotate(member_count=Count('members')).order_by('-created_at')
    family_list = []
    for f in families:
        members = LineUser.objects.filter(family=f)
        patient = members.filter(role='patient').first()
        caregivers = members.filter(role='caregiver')
        family_list.append({
            'group': f,
            'patient': patient,
            'caregivers': caregivers,
            'count': members.count()
        })
    return render(request, 'doctor/families.html', {'families': family_list})

@login_required(login_url='doctor-login')
def doctor_users(request):
    """LINE Users List & Role Management View"""
    users = LineUser.objects.select_related('family').order_by('-registered_at')
    return render(request, 'doctor/users.html', {'users': users})

@login_required(login_url='doctor-login')
def doctor_knowledge(request):
    """Knowledge Articles Management View"""
    articles = KnowledgeArticle.objects.select_related('category').order_by('order')
    return render(request, 'doctor/knowledge.html', {'articles': articles})

@login_required(login_url='doctor-login')
def doctor_faq(request):
    """FAQ Management View"""
    faqs = FAQ.objects.order_by('order')
    return render(request, 'doctor/faq.html', {'faqs': faqs})

@login_required(login_url='doctor-login')
def doctor_notifications(request):
    """Notification Logs View"""
    logs = NotificationLog.objects.select_related('user').order_by('-created_at')[:100]
    return render(request, 'doctor/notifications.html', {'logs': logs})

@login_required(login_url='doctor-login')
def api_patient_detail(request, user_id):
    """API Endpoint returning JSON data for Patient Side Drawer Modal"""
    try:
        patient = LineUser.objects.select_related('family').get(id=user_id, role='patient')
    except LineUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'ไม่พบข้อมูลผู้ป่วย'}, status=404)
        
    family_members = []
    if patient.family:
        members = LineUser.objects.filter(family=patient.family)
        for m in members:
            family_members.append({
                'name': m.name,
                'role_display': m.get_role_display(),
                'phone': m.phone_number or '-',
                'line_display': m.display_name
            })
            
    daily_checks = DailyCheck.objects.filter(user=patient).order_by('-date')[:10]
    checks_data = []
    for dc in daily_checks:
        checks_data.append({
            'date': dc.date.strftime('%Y-%m-%d'),
            'result_level': dc.result_level,
            'result_display': dc.get_result_level_display(),
            'has_fever': dc.has_fever,
            'fever_detail': dc.fever_detail,
            'has_wound': dc.has_wound,
            'wound_detail': dc.wound_detail,
            'has_breathless': dc.has_breathless,
            'breathless_detail': dc.breathless_detail,
            'has_confused': dc.has_confused,
            'confused_detail': dc.confused_detail,
            'has_less_eat': dc.has_less_eat,
            'less_eat_detail': dc.less_eat_detail,
            'responder': dc.get_responder_display(),
        })
        
    vitals = VitalSign.objects.filter(user=patient).order_by('date')[:10]
    vitals_data = []
    for v in vitals:
        vitals_data.append({
            'date': v.date.strftime('%d/%m/%Y'),
            'temp': v.temperature,
            'hr': v.heart_rate,
            'sbp': v.systolic_bp,
            'dbp': v.diastolic_bp,
            'rr': v.respiratory_rate,
            'spo2': v.spo2,
        })
        
    screening = SepsisScreening.objects.filter(user=patient).order_by('-date').first()
    screening_data = None
    if screening:
        screening_data = {
            'date': screening.date.strftime('%Y-%m-%d'),
            'has_red_flag': screening.has_red_flag,
            'has_amber_flag': screening.has_amber_flag,
            'result': screening.result or '',
            'red_flags': {
                'mental': screening.red_flag_mental,
                'rr_ge25': screening.red_flag_rr_ge25,
                'o2_need': screening.red_flag_o2_need,
                'sbp_le90': screening.red_flag_sbp_le90,
                'hr_gt130': screening.red_flag_hr_gt130,
                'no_urine_18h': screening.red_flag_no_urine_18h,
                'skin_change': screening.red_flag_skin_change,
            }
        }

    return JsonResponse({
        'status': 'success',
        'patient': {
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'phone': patient.phone_number or '-',
            'id_card': patient.id_card,
            'family_code': patient.family.code if patient.family else '-',
            'underlying_disease': patient.underlying_disease or '',
            'allergy': patient.allergy or '',
        },
        'family_members': family_members,
        'daily_checks': checks_data,
        'vitals': vitals_data,
        'screening': screening_data
    })

@login_required(login_url='doctor-login')
def api_update_patient_notes(request, user_id):
    """API Endpoint to let doctors save clinical notes for a patient"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient = LineUser.objects.get(id=user_id, role='patient')
            patient.underlying_disease = data.get('underlying_disease', patient.underlying_disease)
            patient.allergy = data.get('allergy', patient.allergy)
            patient.save()
            return JsonResponse({'status': 'success', 'message': 'บันทึกข้อมูลสำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
