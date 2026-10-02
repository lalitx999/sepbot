from django.db import models
from django.utils import timezone
from accounts.models import LineUser, FamilyGroup

class NotificationLog(models.Model):
    TYPE_CHOICES = (
        ('daily_check', 'เตือนเช็คอาการประจำวัน (09:00)'),
        ('sepsis_edu', 'ความรู้เซพซิสประจำสัปดาห์ (จ./พฤ.)'),
        ('non_response', 'เตือนติดตามเมื่อไม่ตอบแบบประเมิน'),
        ('emergency', 'แจ้งเตือนเคสฉุกเฉิน (Red/Yellow Flag)'),
        ('vital_sign', 'เตือนบันทึกสัญญาณชีพ (วันที่ 14/30)'),
    )

    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name='notifications', verbose_name="ผู้รับ")
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='notifications', verbose_name="กลุ่มครอบครัว")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="ประเภทการแจ้งเตือน")
    message = models.TextField(verbose_name="ข้อความที่ส่ง")
    is_sent = models.BooleanField(default=False, verbose_name="ส่งสำเร็จแล้ว")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="เวลาที่ส่งสำเร็จ")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="วันที่สร้างรายการ")

    class Meta:
        db_table = 'notification_notificationlog'
        verbose_name = 'บันทึกการแจ้งเตือน'
        verbose_name_plural = 'บันทึกการแจ้งเตือน (Notification Logs)'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_sent']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Noti [{self.get_type_display()}] -> {self.user.name} (Sent: {self.is_sent})"
