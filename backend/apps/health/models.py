from django.db import models
from django.utils import timezone
from accounts.models import LineUser, FamilyGroup

class VitalSign(models.Model):
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name='vital_signs', verbose_name="ผู้ป่วย")
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='vital_signs', verbose_name="กลุ่มครอบครัว")
    date = models.DateField(default=timezone.now, verbose_name="วันที่บันทึก")

    temperature = models.FloatField(blank=True, null=True, verbose_name="อุณหภูมิกาย (°C)")
    heart_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name="อัตราการเต้นของหัวใจ (ครั้ง/นาที)")
    systolic_bp = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความดันตัวบน (mmHg)")
    diastolic_bp = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความดันตัวล่าง (mmHg)")
    respiratory_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name="อัตราการหายใจ (ครั้ง/นาที)")
    spo2 = models.PositiveIntegerField(blank=True, null=True, verbose_name="ความอิ่มตัวของออกซิเจน SpO2 (%)")

    CONSCIOUSNESS_CHOICES = (
        ('confused', 'สับสน (กระสับกระส่ายที่เพิ่งเกิดขึ้น)'),
        ('alert', 'ตื่นดี (พูดคุยรู้เรื่อง)'),
        ('drowsy', 'ซึม (แต่เรียกแล้วตาสลึมลือ)'),
        ('stupor', 'ซึมมาก (ต้องกระตุ้นจึงจะลืมตา)'),
        ('unconscious', 'ไม่รู้สึกตัว (แม้จะกระตุ้นแล้วก็ตาม)'),
    )
    consciousness = models.CharField(max_length=20, choices=CONSCIOUSNESS_CHOICES, blank=True, null=True, verbose_name="ความรู้สึกตัว")

    URINE_OUTPUT_CHOICES = (
        ('le_500', 'น้อยกว่าหรือเท่ากับ 500 มิลลิลิตร'),
        ('501_999', '501-999 มิลลิลิตร'),
        ('ge_1000', 'มากกว่าหรือเท่ากับ 1,000 มิลลิลิตร'),
    )
    urine_output = models.CharField(max_length=20, choices=URINE_OUTPUT_CHOICES, blank=True, null=True, verbose_name="ปริมาณปัสสาวะต่อวัน")

    recorded_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาที่บันทึก")

    mews_score = models.IntegerField(default=0, blank=True, null=True, verbose_name="คะแนน MEWS")
    mews_level = models.CharField(max_length=10, default='green', blank=True, null=True, verbose_name="ระดับความเสี่ยง MEWS")

    class Meta:
        db_table = 'health_vitalsign'
        verbose_name = 'บันทึกสัญญาณชีพ'
        verbose_name_plural = 'บันทึกสัญญาณชีพ (Vital Signs)'
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"VitalSign {self.user.name} ({self.date}) - Temp:{self.temperature}°C HR:{self.heart_rate}"

