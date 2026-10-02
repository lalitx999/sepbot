from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'ความรู้ทั่วไป (General)'),
        ('medication', 'การใช้ยาและการดูแล (Medication)'),
        ('emergency', 'อาการฉุกเฉิน (Emergency)'),
        ('recovery', 'การฟื้นฟูร่างกาย (Recovery)'),
    )

    question = models.CharField(max_length=200, verbose_name="คำถาม")
    answer = models.TextField(verbose_name="คำตอบ")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general', verbose_name="หมวดหมู่คำถาม")
    order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดงผล")

    class Meta:
        db_table = 'faq_faq'
        verbose_name = 'คำถาม-คำตอบ (FAQ)'
        verbose_name_plural = 'คำถาม-คำตอบ (FAQ 33 ข้อ)'
        ordering = ['order', 'id']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.question}"
