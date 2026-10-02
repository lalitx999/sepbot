# 📋 สรุปภาพรวมโครงการ Sepsis Care Line Chatbot (SUMMARY.md)

ระบบติดตามและส่งเสริมการดูแลตนเองสำหรับผู้ป่วยสูงอายุหลังภาวะเซพซิส (Sepsis Care Line Chatbot System)
**พัฒนาขึ้นตามดุษฎีนิพนธ์ คณะพยาบาลศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย (นางสาวณัฏฐณิชา สิงห์จาน)**

---

## 🛠️ เทคโนโลยีหลักที่ใช้ในโครงการ (Tech Stack)

* **Backend Framework**: Django 4.2 (Django REST Framework)
* **Language & Runtime**: Python 3.14 (พร้อม Monkeypatch แก้ไขปัญหา Context Copying)
* **Database**: PostgreSQL 15 (`sepbot_db`)
* **Task Queue & Scheduler**: Celery 5 + Redis 7 + Django Celery Beat
* **Frontend (LIFF & Web Base)**: HTML5, JavaScript, Vanilla CSS, Bootstrap 5.3, Bootstrap Icons, Google Fonts (`Noto Serif Thai`)
* **Containerization**: Docker & Docker Compose (`docker-compose.yml`)

---

## 🗄️ โครงสร้างฐานข้อมูล 10 ตาราง (PostgreSQL Models)

1. `FamilyGroup`: กลุ่มครอบครัวผู้ป่วยและผู้ดูแล (รหัส `FGxxxxx`)
2. `LineUser`: ผู้ใช้งาน LINE (คนไข้ / ผู้ดูแลหลัก / ผู้ดูแลสำรอง)
3. `DailyCheck`: แบบเช็คอาการประจำวัน (เขียว 🟢 / เหลือง 🟡 / แดง 🔴)
4. `SepsisScreening`: แบบคัดกรองเซพซิส (Risk factors, Red Flags, Amber Flags)
5. `VitalSign`: บันทึกสัญญาณชีพ (Temp, BP, HR, RR, SpO₂) วันที่ 14 และ 30 หลังจำหน่าย
6. `KnowledgeCategory`: หมวดหมู่บทความความรู้ 7 หมวด
7. `KnowledgeArticle`: บทความความรู้ 8 บทเรียนตามคู่มือจุฬาฯ (`guid.md`)
8. `Image`: รูปภาพอินโฟกราฟิกคู่มือจุฬาฯ 44 รูป
9. `FAQ`: คำถามที่พบบ่อย 33 ข้อ พร้อม Keyword Matching Search Engine
10. `NotificationLog`: บันทึกประวัติการส่งแจ้งเตือนและตามเคสผู้ดูแล

---

## 🔗 สรุปรายการ URLs & APIs ทั้งหมดในระบบ

### 1. หน้าเว็บ LIFF Web Application & Web Gallery
* 📝 **ลงทะเบียนผู้ใช้งาน**: `http://localhost:8000/liff/register/`
* 🩺 **เช็คอาการประจำวัน**: `http://localhost:8000/liff/daily-check/`
* 🚨 **คัดกรองเซพซิส**: `http://localhost:8000/liff/screening/`
* 📊 **บันทึกสัญญาณชีพ**: `http://localhost:8000/liff/vitals/`
* 📖 **คลังความรู้ & E-Book Gallery**: `http://localhost:8000/api/v1/knowledge/web/`
* 🛡️ **Django Admin Dashboard**: `http://localhost:8000/admin/` (User: `admin` / Pass: `adminpass`)

### 2. REST API Endpoints
* `POST /api/v1/accounts/register/` - ลงทะเบียนผู้ป่วย/ผู้ดูแล
* `GET /api/v1/accounts/profile/<line_user_id>/` - ดูโปรไฟล์ผู้ใช้
* `GET /api/v1/accounts/family/<family_code>/` - ดึงรายชื่อสมาชิกในครอบครัว
* `POST /api/v1/assessment/daily-check/` - ส่งผลเช็คอาการประจำวัน
* `POST /api/v1/assessment/screening/` - ส่งผลคัดกรองเซพซิส
* `POST /api/v1/health/vitals/` - ส่งผลบันทึกสัญญาณชีพ
* `GET /api/v1/knowledge/articles/` - ดึงรายการบทความความรู้
* `POST /api/v1/faq/search/` - ค้นหา FAQ ด้วย Keyword Search Engine
* `POST /api/v1/line/webhook/` - LINE Messaging API Webhook Handler

---

## 📖 เนื้อหาคลังความรู้คู่มือจุฬาฯ 8 บทเรียน & รูปภาพ 44 รูป

* **บทที่ 1**: ความรู้พื้นฐานเกี่ยวกับภาวะเซพซิส (Sepsis, สาเหตุ, กลุ่มเสี่ยง)
* **บทที่ 2**: การฟื้นตัวและกลุ่มอาการหลังภาวะเซพซิส (Post-Sepsis Syndrome: PSS)
* **บทที่ 3**: การสังเกตอาการและการเฝ้าระวังภาวะทรุดลงทางคลินิก (สัญญาณอันตราย & หน้าที่ผู้ดูแล)
* **บทที่ 4**: การป้องกันการติดเชื้อซ้ำ สุขอนามัย และตารางวัคซีนผู้สูงอายุ (ไข้หวัดใหญ่, โควิด, ปอดอักเสบ, งูสวัด)
* **บทที่ 5**: การใช้ยาอย่างปลอดภัย การทานยาปฏิชีวนะให้ครบ และอาการแพ้ยารุนแรง
* **บทที่ 6 & 7**: โภชนาการฟื้นฟู การออกกำลังกายอย่างเหมาะสม และการป้องกันการหกล้ม
* **บทที่ 8**: การวางแผนระยะยาวและการใช้งาน LINE Chatbot (เขียว/เหลือง/แดง)
* 🖼️ **Infographic E-Book Gallery**: รูปภาพ 44 รูปจาก `backend/media/knowledge/Ebook` ถูกผูกเข้ากับทั้ง 8 บทเรียน รองรับการเปิดสไลด์บนมือถือ (Touch Swipe, Thumbnail Strip, Fullscreen Zoom)

---

## 🧪 ผลการทดสอบระบบ (Automated Tests)

```text
Found 9 test(s).
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.073s

OK
```
> 🎉 **ผลการทดสอบ API และความถูกต้องของระบบ: ผ่าน 100% (9/9 Passed)**

---

## 🚀 ขั้นตอนการนำไป Deploy บน Home Server (Docker Compose)

1. **ย้ายไฟล์โครงการเข้า Home Server** และสั่งสร้าง Container:
   ```bash
   docker compose up -d --build
   ```
   *(ระบบจะทำการสั่ง `migrate`, `collectstatic`, และรัน Seed ข้อมูล FAQ 33 ข้อ + บทเรียนจุฬาฯ 8 บท + รูปภาพ 44 รูปให้อัตโนมัติทันทีที่ Container เริ่มทำงาน!)*

2. **สร้าง Superuser สำหรับเข้า Django Admin** (ทำครั้งเดียว):
   ```bash
   docker exec -it sepbot_web python manage.py createsuperuser
   ```

---

## 🎨 งานที่จะทำต่อในวันพรุ่งนี้

* ออกแบบและประกอบภาพ **Rich Menu 6 ปุ่มภาษาไทย** (ขนาด `2500 x 1686 px`)
* นำ `LINE_CHANNEL_SECRET` และ `LINE_CHANNEL_ACCESS_TOKEN` มากรอกใน `.env` เพื่อทดสอบสลับ Rich Menu อัตโนมัติเมื่อคนไข้ลงทะเบียนสำเร็จ

---
*จัดทำและสรุปข้อมูลโดย Antigravity AI Assistant (Google DeepMind Team)*
