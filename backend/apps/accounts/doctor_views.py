from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Max, Prefetch, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import json

from accounts.models import LineUser, FamilyGroup
from assessment.models import DailyCheck, SepsisScreening
from health.models import VitalSign
from knowledge.models import KnowledgeArticle, KnowledgeCategory
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
    """Vital Signs Tracker Management View with Pagination"""
    vitals_qs = VitalSign.objects.select_related('user', 'family').order_by('-date', '-recorded_at')
    paginator = Paginator(vitals_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor/vitals.html', {'page_obj': page_obj, 'total_count': vitals_qs.count()})

@login_required(login_url='doctor-login')
def doctor_screenings(request):
    """Sepsis Screening Management View with Pagination"""
    screenings_qs = SepsisScreening.objects.select_related('user', 'family').order_by('-date')
    paginator = Paginator(screenings_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor/screenings.html', {'page_obj': page_obj, 'total_count': screenings_qs.count()})

@login_required(login_url='doctor-login')
def doctor_daily_checks(request):
    """Daily Symptom Checks Log View with Pagination"""
    checks_qs = DailyCheck.objects.select_related('user', 'family').order_by('-date', '-responded_at')
    paginator = Paginator(checks_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor/daily_checks.html', {'page_obj': page_obj, 'total_count': checks_qs.count()})

@login_required(login_url='doctor-login')
def doctor_families(request):
    """Family Groups Management View with Pagination"""
    families_qs = FamilyGroup.objects.annotate(member_count=Count('members')).order_by('-created_at')
    paginator = Paginator(families_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    family_list = []
    for f in page_obj:
        members = LineUser.objects.filter(family=f)
        patient = members.filter(role='patient').first()
        caregivers = members.filter(role='caregiver')
        family_list.append({
            'group': f,
            'patient': patient,
            'caregivers': caregivers,
            'count': members.count()
        })
    return render(request, 'doctor/families.html', {'family_list': family_list, 'page_obj': page_obj, 'total_count': families_qs.count()})

@login_required(login_url='doctor-login')
def doctor_users(request):
    """LINE Users List & Role Management View with Pagination"""
    users_qs = LineUser.objects.select_related('family').order_by('-registered_at')
    paginator = Paginator(users_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    families = FamilyGroup.objects.order_by('-created_at')
    return render(request, 'doctor/users.html', {'page_obj': page_obj, 'total_count': users_qs.count(), 'families': families})

@login_required(login_url='doctor-login')
def doctor_knowledge(request):
    """Knowledge Articles Management View (Fixed & Paginator added)"""
    articles_qs = KnowledgeArticle.objects.select_related('category').order_by('category__order', 'id')
    paginator = Paginator(articles_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    categories = KnowledgeCategory.objects.all()
    return render(request, 'doctor/knowledge.html', {'page_obj': page_obj, 'total_count': articles_qs.count(), 'categories': categories})

@login_required(login_url='doctor-login')
def doctor_faq(request):
    """FAQ Management View with Pagination"""
    faqs_qs = FAQ.objects.order_by('order', 'id')
    paginator = Paginator(faqs_qs, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor/faq.html', {'page_obj': page_obj, 'total_count': faqs_qs.count()})

@login_required(login_url='doctor-login')
def doctor_notifications(request):
    """Notification Logs View with Pagination"""
    logs_qs = NotificationLog.objects.select_related('user').order_by('-created_at')
    paginator = Paginator(logs_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'doctor/notifications.html', {'page_obj': page_obj, 'total_count': logs_qs.count()})

# --- CRUD APIs for Clinical Portal ---

@login_required(login_url='doctor-login')
def api_knowledge_save(request):
    """Create or Update Knowledge Article"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            article_id = data.get('id')
            title = data.get('title')
            content = data.get('content')
            summary = data.get('summary', '')
            category_id = data.get('category_id')
            
            category = get_object_or_404(KnowledgeCategory, id=category_id)
            
            if article_id:
                article = get_object_or_404(KnowledgeArticle, id=article_id)
                article.title = title
                article.content = content
                article.summary = summary
                article.category = category
                article.save()
            else:
                article = KnowledgeArticle.objects.create(
                    title=title, content=content, summary=summary, category=category
                )
            return JsonResponse({'status': 'success', 'message': 'บันทึกบทความความรู้สำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required(login_url='doctor-login')
def api_knowledge_delete(request, article_id):
    """Delete Knowledge Article"""
    if request.method == 'POST':
        try:
            article = get_object_or_404(KnowledgeArticle, id=article_id)
            article.delete()
            return JsonResponse({'status': 'success', 'message': 'ลบบทความเรียบร้อยแล้ว'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required(login_url='doctor-login')
def api_faq_save(request):
    """Create or Update FAQ Item"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            faq_id = data.get('id')
            question = data.get('question')
            answer = data.get('answer')
            category = data.get('category', 'general')
            order = data.get('order', 0)
            
            if faq_id:
                faq = get_object_or_404(FAQ, id=faq_id)
                faq.question = question
                faq.answer = answer
                faq.category = category
                faq.order = order
                faq.save()
            else:
                faq = FAQ.objects.create(
                    question=question, answer=answer, category=category, order=order
                )
            return JsonResponse({'status': 'success', 'message': 'บันทึกข้อมูล FAQ สำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required(login_url='doctor-login')
def api_faq_delete(request, faq_id):
    """Delete FAQ Item"""
    if request.method == 'POST':
        try:
            faq = get_object_or_404(FAQ, id=faq_id)
            faq.delete()
            return JsonResponse({'status': 'success', 'message': 'ลบ FAQ เรียบร้อยแล้ว'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required(login_url='doctor-login')
def api_family_create(request):
    """Generate a new Family Group code"""
    if request.method == 'POST':
        try:
            code = FamilyGroup.generate_unique_code()
            family = FamilyGroup.objects.create(code=code)
            return JsonResponse({'status': 'success', 'message': f'สร้างกลุ่มครอบครัวรหัส {code} สำเร็จ', 'code': code})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required(login_url='doctor-login')
def api_user_update(request, user_id):
    """Update LINE User Profile & Family Assignment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(LineUser, id=user_id)
            user.name = data.get('name', user.name)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.role = data.get('role', user.role)
            user.underlying_disease = data.get('underlying_disease', user.underlying_disease)
            user.allergy = data.get('allergy', user.allergy)
            
            family_id = data.get('family_id')
            if family_id:
                user.family = FamilyGroup.objects.get(id=family_id)
            elif family_id == '':
                user.family = None
                
            user.save()
            return JsonResponse({'status': 'success', 'message': 'อัปเดตข้อมูลผู้ใช้สำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

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
