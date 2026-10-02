from celery import shared_task
from django.utils import timezone
from accounts.models import LineUser
from assessment.models import DailyCheck
from .models import NotificationLog

@shared_task
def send_daily_check_reminder():
    """
    Cron: Runs daily at 09:00 AM.
    Sends Flex Message reminder for DailyCheck to registered patients.
    """
    today = timezone.now().date()
    registered_users = LineUser.objects.filter(is_registered=True, role='patient')

    count = 0
    for user in registered_users:
        # Check if already answered today
        if not DailyCheck.objects.filter(user=user, date=today).exists():
            msg = f"สวัสดีครับคุณ {user.name} 🩺 ได้เวลาเช็คอาการประจำวันแล้วครับ กรุณากดปุ่ม 'เช็คอาการ' บนเมนูด้านล่างเพื่อทำแบบประเมินครับ"
            noti = NotificationLog.objects.create(
                user=user,
                family=user.family,
                type='daily_check',
                message=msg
            )
            # Push message via linebot helper if active
            try:
                from linebot.handlers import push_line_message
                success = push_line_message(user.line_user_id, msg)
                if success:
                    noti.is_sent = True
                    noti.sent_at = timezone.now()
                    noti.save()
            except Exception as e:
                print(f"Daily check push notification error: {e}")

            count += 1
    return f"Daily check reminders queued for {count} users."


@shared_task
def check_non_response_and_escalate():
    """
    Cron: Runs at 09:30 and 10:00 AM.
    Reminds patients (09:30) and alerts caregivers (10:00) if patient hasn't completed DailyCheck.
    """
    today = timezone.now().date()
    patients = LineUser.objects.filter(is_registered=True, role='patient')

    escalated = 0
    for patient in patients:
        if not DailyCheck.objects.filter(user=patient, date=today).exists():
            # Find caregiver in the same family group
            if patient.family:
                caregiver = patient.family.members.filter(role='caregiver').first()
                if caregiver:
                    msg = f"⚠️ แจ้งเตือนผู้ดูแล: วันนี้คุณ {patient.name} ยังไม่ได้ทำแบบประเมินอาการประจำวัน ท่านสามารถช่วยตอบแบบประเมินแทนได้ผ่านเมนูด้านล่างครับ"
                    noti = NotificationLog.objects.create(
                        user=caregiver,
                        family=patient.family,
                        type='non_response',
                        message=msg
                    )
                    try:
                        from linebot.handlers import push_line_message
                        if push_line_message(caregiver.line_user_id, msg):
                            noti.is_sent = True
                            noti.sent_at = timezone.now()
                            noti.save()
                    except Exception as e:
                        print(f"Caregiver escalation error: {e}")
                    escalated += 1

    return f"Caregiver non-response notifications sent for {escalated} families."


@shared_task
def send_vital_sign_reminder_day14_30():
    """
    Cron: Runs daily at 09:00 AM.
    Checks patients who reached Day 14 or Day 30 since registration and sends Vital Sign Reminder.
    """
    today = timezone.now().date()
    registered_patients = LineUser.objects.filter(is_registered=True, role='patient')

    count = 0
    for patient in registered_patients:
        if not patient.registered_at:
            continue
            
        days_passed = (today - patient.registered_at.date()).days
        if days_passed in [14, 30]:
            round_num = 1 if days_passed == 14 else 2
            msg = (
                f"🔔 **แจ้งเตือนบันทึกสัญญาณชีพ (ครั้งที่ {round_num}: วันที่ {days_passed})**\n\n"
                f"สวัสดีค่ะคุณ {patient.name} 🩺 ถึงกำหนดบันทึกสัญญาณชีพ (อุณหภูมิ, ความดัน, ชีพจร, SpO₂) ประจำวันที่ {days_passed} แล้วค่ะ\n\n"
                f"กรุณากดปุ่ม 'บันทึกสุขภาพ' บนเมนูด้านล่างเพื่อกรอกข้อมูลสุขภาพนะคะ 💙"
            )
            
            noti = NotificationLog.objects.create(
                user=patient,
                family=patient.family,
                title=f"บันทึกสัญญาณชีพ วันที่ {days_passed}",
                message=msg,
                alert_type="yellow"
            )
            
            try:
                from linebot.handlers import push_line_message
                if push_line_message(patient.line_user_id, msg):
                    noti.sent_status = True
                    noti.save()
            except Exception as e:
                print(f"Vital Sign reminder push error: {e}")
            count += 1

    return f"Vital Sign Day 14/30 reminders sent to {count} patients."
