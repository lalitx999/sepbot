from django.db import models
from django.utils import timezone
from accounts.models import LineUser, FamilyGroup

class DailyCheck(models.Model):
    RESULT_CHOICES = (
        ('green', 'ปกติ / ดูแลตนเอง (Green)'),
        ('yellow', 'มีอาการเสี่ยง / ติดตาม (Yellow)'),
        ('red', 'อาการรุนแรง / พบแพทย์ด่วน (Red)'),
    )

    RESPONDER_CHOICES = (
        ('patient', 'ผู้ป่วยตอบเอง'),
        ('caregiver_help', 'ผู้ดูแลช่วยตอบ'),
        ('caregiver_replace', 'ผู้ดูแลตอบแทน'),
    )

    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name='daily_checks', verbose_name="ผู้ใช้")
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='daily_checks', verbose_name="กลุ่มครอบครัว")
    date = models.DateField(default=timezone.now, verbose_name="วันที่ประเมิน")
    
    # 5 Daily Assessment Questions
    has_fever = models.BooleanField(default=False, verbose_name="1. มีไข้หรือหนาวสั่น")
    fever_detail = models.CharField(max_length=50, blank=True, null=True, verbose_name="รายละเอียดไข้/อุณหภูมิ")

    has_wound = models.BooleanField(default=False, verbose_name="2. แผลบวม/แดง/มีปวดบวม")
    wound_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name="รายละเอียดแผล")

    has_breathless = models.BooleanField(default=False, verbose_name="3. หายใจเหนื่อย/หอบ")
    breathless_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name="รายละเอียดหายใจ")

    has_confused = models.BooleanField(default=False, verbose_name="4. ซึม/สับสน/ง่วงผิดปกติ")
    confused_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name="รายละเอียดซึม/สับสน")

    has_less_eat = models.BooleanField(default=False, verbose_name="5. ทานอาหาร/ดื่มน้ำได้ลดลงมาก")
    less_eat_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name="รายละเอียดการทาน")

    result_level = models.CharField(max_length=10, choices=RESULT_CHOICES, verbose_name="ระดับผลประเมิน")
    responder = models.CharField(max_length=20, choices=RESPONDER_CHOICES, default='patient', verbose_name="ผู้ตอบแบบประเมิน")
    responded_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาที่ตอบ")

    class Meta:
        db_table = 'assessment_dailycheck'
        verbose_name = 'การประเมินอาการรายวัน'
        verbose_name_plural = 'การประเมินอาการรายวัน (Daily Checks)'
        unique_together = ('user', 'date')
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['result_level']),
        ]

    def __str__(self):
        return f"DailyCheck {self.user.name} ({self.date}) -> {self.result_level}"


class SepsisScreening(models.Model):
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name='sepsis_screenings', verbose_name="ผู้ใช้")
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='sepsis_screenings', verbose_name="กลุ่มครอบครัว")
    date = models.DateField(default=timezone.now, verbose_name="วันที่ประเมิน")

    # Step 1: Risk Factors
    age_over_75 = models.BooleanField(default=False, verbose_name="อายุมากกว่า 75 ปี")
    immunocompromised = models.BooleanField(default=False, verbose_name="ภาวะภูมิคุ้มกันบกพร่อง")
    has_catheter = models.BooleanField(default=False, verbose_name="มีสายสวน/บาดแผลเรื้อรัง")
    recent_surgery = models.BooleanField(default=False, verbose_name="เพิ่งได้รับการผ่าตัด/หัตถการ")

    # Step 2: Infection Source
    infection_respiratory = models.BooleanField(default=False, verbose_name="ติดเชื้อระบบทางเดินหายใจ")
    infection_urinary = models.BooleanField(default=False, verbose_name="ติดเชื้อระบบทางเดินปัสสาวะ")
    infection_skin = models.BooleanField(default=False, verbose_name="ติดเชื้อผิวหนัง/แผล")
    infection_device = models.BooleanField(default=False, verbose_name="ติดเชื้อจากอุปกรณ์ในร่างกาย")
    infection_brain = models.BooleanField(default=False, verbose_name="ติดเชื้อระบบประสาท/สมอง")
    infection_surgery = models.BooleanField(default=False, verbose_name="ติดเชื้อจากการผ่าตัด")
    infection_other = models.CharField(max_length=200, blank=True, null=True, verbose_name="แหล่งติดเชื้ออื่นๆ")

    # Step 3: Red Flags (7 Items)
    red_flag_mental = models.BooleanField(default=False, verbose_name="Red 1: สภาพจิตใจเปลี่ยน/สับสน")
    red_flag_rr_ge25 = models.BooleanField(default=False, verbose_name="Red 2: อัตราหายใจ >= 25 ครั้ง/นาที")
    red_flag_o2_need = models.BooleanField(default=False, verbose_name="Red 3: ต้องให้ออกซิเจน >= 40%")
    red_flag_sbp_le90 = models.BooleanField(default=False, verbose_name="Red 4: ความดันตัวบน <= 90 mmHg")
    red_flag_hr_gt130 = models.BooleanField(default=False, verbose_name="Red 5: ชีพจร > 130 ครั้ง/นาที")
    red_flag_no_urine_18h = models.BooleanField(default=False, verbose_name="Red 6: ไม่ปัสสาวะเลยเกิน 18 ชม.")
    red_flag_skin_change = models.BooleanField(default=False, verbose_name="Red 7: ผิวหนังมีลายด่าง/ซีด grey/mottled")

    # Step 4: Amber Flags (10 Items)
    amber_flag_behavior = models.BooleanField(default=False, verbose_name="Amber 1: พฤติกรรมเปลี่ยนแปลง")
    amber_flag_activity_down = models.BooleanField(default=False, verbose_name="Amber 2: ความสามารถทำกิจกรรมลดลง")
    amber_flag_rr_21_24 = models.BooleanField(default=False, verbose_name="Amber 3: อัตราหายใจ 21-24 ครั้ง/นาที")
    amber_flag_sbp_91_100 = models.BooleanField(default=False, verbose_name="Amber 4: ความดันตัวบน 91-100 mmHg")
    amber_flag_hr_91_120 = models.BooleanField(default=False, verbose_name="Amber 5: ชีพจร 91-120 ครั้ง/นาที")
    amber_flag_spo2_lt92 = models.BooleanField(default=False, verbose_name="Amber 6: SpO2 < 92%")
    amber_flag_no_urine_12_18h = models.BooleanField(default=False, verbose_name="Amber 7: ไม่ปัสสาวะ 12-18 ชม.")
    amber_flag_immuno = models.BooleanField(default=False, verbose_name="Amber 8: สงสัยติดเชื้อร่วมกับภูมิบกพร่อง")
    amber_flag_infection_sign = models.BooleanField(default=False, verbose_name="Amber 9: สัญญาณติดเชื้อเฉพาะที่ชัดเจน")
    amber_flag_temp_lt36 = models.BooleanField(default=False, verbose_name="Amber 10: อุณหภูมิกาย < 36.0°C")

    # Calculated Results
    has_red_flag = models.BooleanField(default=False, verbose_name="พบ Red Flag")
    has_amber_flag = models.BooleanField(default=False, verbose_name="พบ Amber Flag")
    result = models.TextField(blank=True, null=True, verbose_name="คำแนะนำ/สรุปผลการคัดกรอง")

    class Meta:
        db_table = 'assessment_sepsisscreening'
        verbose_name = 'การคัดกรองภาวะเซพซิส'
        verbose_name_plural = 'การคัดกรองภาวะเซพซิส (Sepsis Screenings)'
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['has_red_flag', 'has_amber_flag']),
        ]

    def __str__(self):
        return f"SepsisScreening {self.user.name} ({self.date}) -> Red:{self.has_red_flag} Amber:{self.has_amber_flag}"
