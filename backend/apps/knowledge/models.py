from django.db import models
from django.utils import timezone

class KnowledgeCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (URL)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Emoji / Icon Class")
    order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดงผล")

    class Meta:
        db_table = 'knowledge_knowledgecategory'
        verbose_name = 'หมวดหมู่ความรู้'
        verbose_name_plural = 'หมวดหมู่ความรู้ (Knowledge Categories)'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.icon or ''} {self.name}"


class KnowledgeArticle(models.Model):
    SCHEDULE_CHOICES = (
        ('', 'ไม่ส่งอัตโนมัติ'),
        ('mon_thu', 'ส่งทุกวันจันทร์และพฤหัสบดี (14:00 น.)'),
        ('custom', 'กำหนดเวลาเอง'),
    )

    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='articles', verbose_name="หมวดหมู่")
    title = models.CharField(max_length=200, verbose_name="หัวข้อบทความ")
    content = models.TextField(verbose_name="เนื้อหาบทความ (HTML)")
    summary = models.TextField(blank=True, null=True, verbose_name="สรุปย่อ (Preview)")
    is_published = models.BooleanField(default=True, verbose_name="สถานะเผยแพร่")
    send_schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, blank=True, default='', verbose_name="ตารางส่งแจ้งเตือน")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    class Meta:
        db_table = 'knowledge_knowledgearticle'
        verbose_name = 'บทความความรู้'
        verbose_name_plural = 'บทความความรู้ (Knowledge Articles)'
        ordering = ['id']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_published']),
            models.Index(fields=['send_schedule']),
        ]

    def __str__(self):
        return self.title


class Image(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='images', verbose_name="บทความ")
    image = models.ImageField(upload_to='gallery/', verbose_name="ไฟล์รูปภาพ Infographic")
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="คำอธิบายใต้รูป")
    order = models.PositiveIntegerField(default=0, verbose_name="ลำดับรูปภาพ")

    class Meta:
        db_table = 'knowledge_image'
        verbose_name = 'รูปภาพ Infographic'
        verbose_name_plural = 'รูปภาพ Infographic (Gallery Images)'
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.article.title} (#{self.order})"
