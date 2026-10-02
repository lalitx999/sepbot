from django.db import models
from django.utils import timezone
from accounts.models import LineUser, FamilyGroup

class VitalSign(models.Model):
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name='vital_signs', verbose_name="ผู้ป่วย")
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='vital_signs', verbose_name="กลุ่มครอบครัว")
    date = models.DateField(default=timezone.now, verbose_name="วันที่บันทึก")

    temperature = models.FloatField(blank=True, null=True, verbose_name="อุณหภูมิกาย (°C)")
    heart_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name="อัตราการเต้นของหัวใจ/ชีพจร (ครั้ง/นาที)")
    systolic_bp = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความดันตัวบน (mmHg)")
    diastolic_bp = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความดันตัวล่าง (mmHg)")
    respiratory_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name="อัตราการหายใจ (ครั้ง/นาที)")
    spo2 = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความอิ่มตัวของออกซิเจน SpO2 (%)")

    recorded_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาที่บันทึก")

    class Meta:
        db_table = 'health_vitalsign'
        verbose_name = 'บันทึกสัญญาณชีพ'
        verbose_name_plural = 'บันทึกสัญญาณชีพ (Vital Signs)'
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"VitalSign {self.user.name} ({self.date}) - Temp:{self.temperature}°C SpO2:{self.spo2}%"
