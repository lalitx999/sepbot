from django.shortcuts import render

def liff_register(request):
    """LIFF Registration Form Page"""
    return render(request, 'liff/register.html')

def liff_select_type(request):
    """LIFF Assessment Type Selection Page (Daily Check vs Sepsis Screening)"""
    return render(request, 'liff/select_type.html')

def liff_daily_check(request):
    """LIFF Daily Check Symptom Form Page (Shows choice selection if opened directly from Rich Menu)"""
    mode = request.GET.get('mode')
    if mode != 'direct':
        return render(request, 'liff/select_type.html')
    return render(request, 'liff/daily_check.html')

def liff_screening(request):
    """LIFF Sepsis Screening Form Page"""
    return render(request, 'liff/screening.html')

def liff_vitals(request):
    """LIFF Vital Signs Recording Form Page"""
    return render(request, 'liff/vitals.html')
