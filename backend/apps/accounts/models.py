import random
import string
from django.db import models
from django.utils import timezone

class FamilyGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="รหัสครอบครัว (FGxxxxx)")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="วันที่สร้าง")

    class Meta:
        db_table = 'accounts_familygroup'
        verbose_name = 'กลุ่มครอบครัว'
        verbose_name_plural = 'กลุ่มครอบครัว (Family Groups)'
        ordering = ['-created_at']

    def __str__(self):
        return f"FamilyGroup {self.code}"

    @classmethod
    def generate_unique_code(cls):
        while True:
            numbers = ''.join(random.choices(string.digits, k=5))
            code = f"FG{numbers}"
            if not cls.objects.filter(code=code).exists():
                return code


class LineUser(models.Model):
    ROLE_CHOICES = (
        ('patient', 'ผู้ป่วย (Patient)'),
        ('caregiver', 'ผู้ดูแล (Caregiver)'),
        ('nurse', 'พยาบาล / ทีมวิจัย (Nurse)'),
    )

    line_user_id = models.CharField(max_length=50, unique=True, verbose_name="LINE User ID")
    display_name = models.CharField(max_length=100, verbose_name="ชื่อแสดงใน LINE")
    name = models.CharField(max_length=100, verbose_name="ชื่อ-นามสกุลจริง")
    id_card = models.CharField(max_length=13, verbose_name="เลขบัตรประชาชน 13 หลัก")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="เบอร์โทรศัพท์")
    age = models.PositiveIntegerField(verbose_name="อายุ (ปี)")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="บทบาท")
    family = models.ForeignKey(
        FamilyGroup, 
        on_delete=models.CASCADE, 
        related_name='members',
        null=True, 
        blank=True,
        verbose_name="กลุ่มครอบครัว"
    )
    is_registered = models.BooleanField(default=False, verbose_name="สถานะลงทะเบียน")
    registered_at = models.DateTimeField(default=timezone.now, verbose_name="วันที่ลงทะเบียน")
    
    # Doctor / Nurse Managed Fields (Editable via Django Admin)
    underlying_disease = models.TextField(blank=True, null=True, verbose_name="โรคประจำตัว (หมอ/พยาบาลกรอก)")
    allergy = models.TextField(blank=True, null=True, verbose_name="ประวัติแพ้ยา")

    class Meta:
        db_table = 'accounts_lineuser'
        verbose_name = 'ผู้ใช้งาน LINE'
        verbose_name_plural = 'ผู้ใช้งาน LINE (LINE Users)'
        indexes = [
            models.Index(fields=['line_user_id']),
            models.Index(fields=['family']),
        ]

    def __str__(self):
        role_str = "ผู้ป่วย" if self.role == "patient" else "ผู้ดูแล"
        return f"{self.name} ({role_str}) - LINE: {self.display_name}"
