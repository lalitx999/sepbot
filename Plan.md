ได้เลยครับ! ผมขอจัดเต็มให้คุณวัยรุ่นนนเลย! 🚀

ขอแยกเป็น 2 ไฟล์นะครับ:
1. **`PROJECT_OVERVIEW.md`** - สรุปภาพรวมโครงการ + แผนพัฒนา
2. **`DATABASE_SCHEMA.md`** - รายละเอียดฐานข้อมูลทั้งหมด (ER Diagram + Field อธิบาย)

---

# 📄 ไฟล์ที่ 1: `PROJECT_OVERVIEW.md`

```markdown
# Sepsis Care Line Chatbot - Project Overview

> ระบบแชตบอตสำหรับช่วยเหลือผู้ป่วยภาวะเซพซิสหลังจำหน่ายจากโรงพยาบาล  
> พัฒนาด้วย Django REST Framework + PostgreSQL + LINE Messaging API

---

## 🎯 วัตถุประสงค์ของโครงการ

1. **ลดการกลับเข้ารับการรักษาซ้ำ** ของผู้ป่วย Sepsis หลังจำหน่าย
2. **เสริมพลังผู้ดูแล** ด้วยความรู้และเครื่องมือคัดกรองภาวะ Sepsis
3. **ติดตามอาการผู้ป่วยรายวัน** และแจ้งเตือนทีมแพทย์เมื่อพบความผิดปกติ
4. **ให้ความรู้** เกี่ยวกับ Sepsis และการดูแลตนเองผ่าน Content + Infographic

---

## 👥 กลุ่มเป้าหมาย

| กลุ่ม | บทบาท | ความต้องการ |
|------|-------|------------|
| **ผู้ป่วย Sepsis** | ใช้ Line Bot ประเมินอาการและรับความรู้ | ดูแลตัวเอง, แจ้งเตือนเมื่ออาการแย่ลง |
| **ผู้ดูแลหลัก** | ช่วยตอบแบบประเมิน, รับการแจ้งเตือน | ติดตามอาการ, ตัดสินใจพาไปโรงพยาบาล |
| **ทีมพยาบาล** | รับการแจ้งเตือนจากระบบ (สีเหลือง) | ติดตามผู้ป่วย, ตอบคำถามเฉพาะ |

---

## 🏗️ สถาปัตยกรรมระบบ (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                        ผู้ใช้ (LINE)                         │
│            ผู้ป่วย / ผู้ดูแล / ทีมพยาบาล                     │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS (Webhook)
┌─────────────────────────▼───────────────────────────────────┐
│                    LINE Messaging API                        │
│              (Flex Message / LIFF / Rich Menu)              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Django Backend                          │
├─────────────────────────────────────────────────────────────┤
│  • Webhook Handler (รับข้อความจาก LINE)                     │
│  • REST API (สำหรับ LIFF + Web Base)                       │
│  • Logic ประเมินอาการ (เขียว/เหลือง/แดง)                   │
│  • Scheduler (Celery Beat) ส่ง Noti อัตโนมัติ              │
│  • FAQ Engine (ตอบคำถาม 33 ข้อ)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    PostgreSQL Database                       │
├─────────────────────────────────────────────────────────────┤
│  • User Management (FamilyGroup, LineUser)                  │
│  • Assessment (DailyCheck, SepsisScreening)                 │
│  • Health Monitoring (VitalSign)                            │
│  • Knowledge Management (Articles, Images)                  │
│  • FAQ (33 คำถาม-คำตอบ)                                     │
│  • Notification Logs                                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    External Services                         │
├─────────────────────────────────────────────────────────────┤
│  • Redis (Celery Queue)                                    │
│  • Cloud Storage (รูปภาพ / Infographic)                    │
│  • Nginx (Reverse Proxy + Static/Media)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flow การทำงานหลัก (User Journey)

### 1. Onboarding (การลงทะเบียน)

```
ผู้ใช้ Scan QR Code / Add LINE Official Account
  ↓
รับ Greeting Message (Flex Message) พร้อมปุ่ม "ลงทะเบียน"
  ↓
กดปุ่ม → เปิด LIFF (ลงทะเบียนครั้งแรก)
  ↓
กรอกข้อมูล: ชื่อ-นามสกุล, เลขบัตรประชาชน, อายุ, บทบาท
  ↓
ระบบสร้าง LINE User ID อัตโนมัติ
  ↓
สร้าง FamilyGroup (ผู้ป่วย 1 + ผู้ดูแล 1)
  ↓
เปลี่ยน Rich Menu จาก "รอลงทะเบียน" → "เมนูใช้งาน"
```

### 2. Daily Check (เช็คอาการประจำวัน)

```
LINE ส่ง Notification เวลา 09:00 น.
  ↓
ผู้ป่วยกดปุ่ม "เช็คอาการ" ใน Rich Menu
  ↓
แสดง Flex Message: 5 คำถาม (ไข้, แผล, หายใจ, ซึม, กิน/ดื่ม)
  ↓
ผู้ตอบแบบประเมิน: ผู้ป่วยเอง / ผู้ดูแลช่วย / ผู้ดูแลตอบแทน
  ↓
ระบบประเมินผลเป็น 3 ระดับ
  ↓
┌───────┬─────────────────────────────────────┐
│ สีเขียว │ ไม่มีอาการใดๆ → แนะนำดูแลตนเอง     │
│ สีเหลือง │ มีอาการผิดปกติ → แจ้งพยาบาล        │
│ สีแดง   │ อาการรุนแรง → โทร 1669 ทันที       │
└───────┴─────────────────────────────────────┘
  ↓
บันทึกผล + ส่งข้อความตอบกลับผู้ใช้
```

### 3. Sepsis Screening (คัดกรองภาวะเซพซิส)

```
ผู้ใช้กด "คัดกรองเซพซิส" ในเมนู
  ↓
เปิด Web Base หรือ LIFF (แบบประเมิน 4 ขั้นตอน)
  ↓
Step 1: ปัจจัยเสี่ยง (อายุ >75, ภูมิคุ้มกัน, สายสวน, ผ่าตัด)
  ↓
Step 2: แหล่งติดเชื้อ (ระบบหายใจ/ปัสสาวะ/ผิวหนัง/ฯลฯ)
  ↓
Step 3: Red Flags (7 อาการรุนแรง)
  ↓
Step 4: Amber Flags (10 อาการที่ต้องเฝ้าระวัง)
  ↓
สรุปผล + คำแนะนำ (ไปโรงพยาบาล / ติดตามใกล้ชิด)
```

### 4. Health Monitoring (บันทึกสุขภาพ)

```
วันที่ 14 และ 30 หลังจำหน่าย
  ↓
LINE ส่ง Notification เตือนให้บันทึกสัญญาณชีพ
  ↓
ผู้ใช้กด "บันทึกสุขภาพ" ใน Rich Menu
  ↓
กรอกข้อมูล: อุณหภูมิ, ชีพจร, ความดัน, อัตราการหายใจ, SpO₂
  ↓
บันทึกในระบบ
```

### 5. Sepsis Education (เรียนรู้เซพซิส)

```
LINE ส่ง Content อัตโนมัติ วันจันทร์และพฤหัส เวลา 14:00 น.
  ↓
ผู้ใช้กด "เรียนรู้เพิ่มเติม" ใน Rich Menu
  ↓
เปิด Web Base: แสดงหมวดหมู่ความรู้
  ↓
กดเลือกหัวข้อ → แสดงบทความ + Photo Gallery (Infographic)
  ↓
เนื้อหา: ความรู้พื้นฐาน, การฟื้นตัว, สัญญาณเตือน, การป้องกัน
```

### 6. Ask a Nurse (ถามพยาบาล)

```
ผู้ใช้พิมพ์คำถาม (หรือเลือกจาก FAQ)
  ↓
Bot ตรวจสอบ Keyword → ตอบจากฐานข้อมูล FAQ 33 ข้อ
  ↓
ถ้าไม่ใช่ FAQ → แสดงข้อความ: "กรุณาติดต่อพยาบาล"
  ↓
กดปุ่ม "ติดต่อพยาบาล" → ส่ง Line Message ไปยังทีมวิจัย
```

### 7. Emergency (ติดต่อฉุกเฉิน)

```
ผู้ใช้กด "ติดต่อฉุกเฉิน" ใน Rich Menu
  ↓
แสดง Alert สีแดง + เบอร์โทรฉุกเฉิน
  ↓
┌─────────────────────────────────────────┐
│ 🚨 อาการที่ต้องโทร 1669 ทันที:          │
│ • พูดไม่ชัดหรือสับสน                    │
│ • หนาวสั่นอย่างรุนแรง                   │
│ • ไม่มีปัสสาวะเลย (ทั้งวัน)              │
│ • หายใจลำบากอย่างรุนแรง                │
│ • รู้สึกเหมือนกำลังจะตาย                │
│ • ผิวหนังมีลายด่างสีเทาซีด              │
├─────────────────────────────────────────┤
│ 📞 เบอร์โทรฉุกเฉิน:                     │
│ • การแพทย์ฉุกเฉิน: 1669                 │
│ • เหตุด่วนเหตุร้าย: 191                  │
│ • รพ.จุฬาลงกรณ์: 022564000             │
│ • พยาบาลโครงการ: 0996244555            │
└─────────────────────────────────────────┘
```

---

## 📱 Rich Menu Design

### เมนูที่ 1: "รอลงทะเบียน" (ก่อนลงทะเบียน)
```
┌─────────────────────┐
│   📝 ลงทะเบียน       │
│  กดเพื่อเริ่มใช้งาน   │
└─────────────────────┘
```

### เมนูที่ 2: "เมนูใช้งาน" (6 ปุ่ม หลังลงทะเบียน)
```
┌──────────┬──────────┬──────────┐
│  🩺      │  📊      │  📚      │
│ เช็คอาการ │ บันทึก   │ การดูแล  │
│          │ สุขภาพ   │ ตนเอง    │
├──────────┼──────────┼──────────┤
│  📖      │  💬      │  🚨      │
│ เรียนรู้  │ ถาม      │ ติดต่อ   │
│ เพิ่มเติม │ พยาบาล   │ ฉุกเฉิน  │
└──────────┴──────────┴──────────┘
```

---

## 🕐 Scheduler (การแจ้งเตือนอัตโนมัติ)

| เวลา | กิจกรรม | เป้าหมาย |
|------|---------|---------|
| **ทุกวัน 09:00 น.** | ส่ง Notification "เช็คอาการประจำวัน" | ผู้ป่วยทุกคน |
| **จันทร์ & พฤหัส 14:00 น.** | ส่งความรู้ Sepsis (บทความสั้น + Infographic) | ผู้ป่วย + ผู้ดูแล |
| **ถ้าผู้ป่วยไม่ตอบ 09:00 น.** | เตือนครั้งที่ 1 (09:30) | ผู้ป่วย |
| **ถ้ายังไม่ตอบ** | เตือนครั้งที่ 2 (10:00) | ผู้ดูแลหลัก |
| **วันที่ 14 & 30** | เตือนบันทึกสัญญาณชีพ | ผู้ป่วย |

---

## 🛠️ Tech Stack รายละเอียด

| Component | Technology | Version | เหตุผลที่เลือก |
|-----------|------------|---------|---------------|
| **Backend Framework** | Django | 4.2+ | มี Admin, ORM, Security ในตัว |
| **API** | Django REST Framework | 3.14+ | สร้าง REST API รวดเร็ว |
| **Database** | PostgreSQL | 15+ | รองรับ JSON, ACID, เชื่อถือได้ |
| **Cache/Queue** | Redis | 7+ | ใช้กับ Celery |
| **Scheduler** | Celery + Celery Beat | 5.3+ | จัดการงานประจำ |
| **LINE Integration** | line-bot-sdk-python | 3.5+ | Official SDK |
| **Web Server** | Nginx | Alpine | Reverse Proxy + Static |
| **Container** | Docker + Docker Compose | Latest | Deploy สะดวก |
| **Frontend (Web Base)** | Django Template + Bootstrap 5 | 5.3+ | ง่าย, ใช้ร่วมกับ Django ได้ |
| **Photo Gallery** | Lightbox2 / Fancybox | Latest | แสดง Infographic |
| **Version Control** | Git + GitHub | - | เก็บประวัติโค้ด |
| **Testing** | pytest / Django Test | - | ทดสอบ API |

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```
sepbot/                                    # Project Root
├── docker-compose.yml                     # Docker Compose
├── .env                                   # Environment Variables
├── .gitignore                             # Git Ignore
├── README.md                              # คำอธิบายโปรเจกต์
├── requirements.txt                       # Python Dependencies
│
├── backend/                               # Django Backend
│   ├── Dockerfile                         # Docker Image
│   ├── manage.py                          # Django Management
│   ├── sepbot/                            # Project Config
│   │   ├── __init__.py
│   │   ├── settings.py                    # Settings
│   │   ├── urls.py                        # Root URL
│   │   ├── wsgi.py
│   │   └── celery.py                      # Celery Config
│   │
│   ├── apps/                              # Django Apps
│   │   ├── accounts/                      # การจัดการผู้ใช้
│   │   │   ├── models.py                  # FamilyGroup, LineUser
│   │   │   ├── views.py                   # Register, Profile
│   │   │   ├── serializers.py             # DRF Serializers
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   │
│   │   ├── assessment/                    # การประเมินอาการ
│   │   │   ├── models.py                  # DailyCheck, SepsisScreening
│   │   │   ├── views.py                   # DailyCheck, Screening
│   │   │   ├── services.py                # Logic ประเมินผล
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   │
│   │   ├── health/                        # บันทึกสุขภาพ
│   │   │   ├── models.py                  # VitalSign
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── admin.py
│   │   │
│   │   ├── knowledge/                     # ความรู้ + Gallery
│   │   │   ├── models.py                  # Category, Article, Image
│   │   │   ├── views.py                   # แสดงบทความ
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   └── templates/                 # Django Templates
│   │   │       └── knowledge/
│   │   │           ├── list.html          # รายการบทความ
│   │   │           └── detail.html        # บทความ + Gallery
│   │   │
│   │   ├── faq/                           # FAQ 33 ข้อ
│   │   │   ├── models.py                  # FAQ
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   │
│   │   ├── linebot/                       # LINE Webhook
│   │   │   ├── views.py                   # Webhook Handler
│   │   │   ├── handlers.py                # Message Handlers
│   │   │   ├── rich_menu.py               # Rich Menu Management
│   │   │   ├── flex_messages.py           # Flex Message Templates
│   │   │   └── urls.py
│   │   │
│   │   └── notification/                  # การแจ้งเตือน
│   │       ├── models.py                  # NotificationLog
│   │       ├── tasks.py                   # Celery Tasks
│   │       └── admin.py
│   │
│   ├── static/                            # Static Files (CSS, JS)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── media/                             # Media Files (Upload)
│       └── gallery/                       # รูปภาพ Infographic
│
├── nginx/                                 # Nginx Config
│   └── default.conf
│
├── scripts/                               # Utility Scripts
│   ├── init_db.sql                        # SQL Init
│   ├── seed_faq.py                        # ใส่ FAQ 33 ข้อ
│   ├── seed_knowledge.py                  # ใส่เนื้อหาความรู้
│   └── create_rich_menu.py                # สร้าง Rich Menu
│
└── docs/                                  # เอกสาร
    ├── PROJECT_OVERVIEW.md                # ไฟล์นี้
    └── DATABASE_SCHEMA.md                 # รายละเอียดฐานข้อมูล
```

---

## 🗺️ Roadmap การพัฒนา (แบ่งเป็น Phase)

### Phase 0: Setup (Day 1) ✅
- [ ] ติดตั้ง Docker + Docker Compose
- [ ] สร้าง Django Project + Apps
- [ ] ตั้งค่า PostgreSQL + Redis
- [ ] สร้าง Models ทั้งหมด
- [ ] Migrate ฐานข้อมูล

### Phase 1: LINE Integration (Day 2)
- [ ] ตั้งค่า LINE Official Account
- [ ] สร้าง LIFF App
- [ ] สร้าง Webhook Endpoint
- [ ] สร้าง Rich Menu (2 แบบ)
- [ ] ทดสอบ Webhook รับ-ส่งข้อความ

### Phase 2: Onboarding (Day 3)
- [ ] พัฒนา LIFF ลงทะเบียน
- [ ] สร้าง API Register
- [ ] สร้าง FamilyGroup อัตโนมัติ
- [ ] เปลี่ยน Rich Menu หลังลงทะเบียน
- [ ] ทดสอบ End-to-End

### Phase 3: Daily Check (Day 4-5)
- [ ] สร้าง Flex Message สำหรับ 5 คำถาม
- [ ] พัฒนา Logic ประเมินผล (เขียว/เหลือง/แดง)
- [ ] เชื่อมต่อ API DailyCheck
- [ ] ตั้ง Scheduler (09:00 น.)
- [ ] สร้างระบบ Non-response Detection

### Phase 4: Sepsis Screening (Day 6)
- [ ] สร้างหน้า LIFF หรือ Web Base
- [ ] พัฒนา Logic Red Flag / Amber Flag
- [ ] สรุปผล + แนะนำ
- [ ] ทดสอบแบบประเมิน

### Phase 5: Knowledge + Gallery (Day 7)
- [ ] สร้าง Django Template สำหรับ Web Base
- [ ] สร้าง Model Knowledge + Images
- [ ] ใช้ Lightbox/Fancybox แสดง Gallery
- [ ] ใส่เนื้อหาความรู้ Sepsis
- [ ] ตั้ง Scheduler (จันทร์/พฤหัส 14:00)

### Phase 6: FAQ + Nurse (Day 8)
- [ ] ใส่ FAQ 33 ข้อในฐานข้อมูล
- [ ] พัฒนา Keyword Matching หรือ RAG
- [ ] สร้างปุ่ม "ติดต่อพยาบาล"
- [ ] เชื่อมต่อกับทีมวิจัย

### Phase 7: Health Monitoring (Day 9)
- [ ] สร้าง API VitalSign
- [ ] สร้าง LIFF หรือ Flex Message
- [ ] ตั้ง Scheduler (วันที่ 14, 30)

### Phase 8: Testing + Deployment (Day 10)
- [ ] ทดสอบระบบทั้งหมด
- [ ] ทดสอบ Stress Test (Celery)
- [ ] Deploy ขึ้น Home Server
- [ ] ตั้งค่า HTTPS (Let's Encrypt)
- [ ] เปิดให้ใช้งานจริง

---

## ⚠️ ความเสี่ยงและแนวทางแก้ไข

| ความเสี่ยง | ผลกระทบ | แนวทางแก้ไข |
|-----------|---------|------------|
| LINE Webhook ต้องใช้ HTTPS | ไม่สามารถทดสอบในเครื่องได้ | ใช้ Ngrok หรือ Cloudflare Tunnel |
| Celery Beat ต้องการ Redis | ระบบไม่ส่ง Noti | ใช้ APScheduler เป็นตัวเลือกสำรอง |
| LIFF ต้องใช้ HTTPS เช่นกัน | เปิดหน้าเว็บไม่ได้ | ใช้ Ngrok + Django Debug Mode |
| ผู้ใช้ไม่ตอบแบบประเมิน | ขาดข้อมูลการติดตาม | ระบบเตือนซ้ำ + แจ้งผู้ดูแล |
| LLM (FAQ) มีค่าใช้จ่าย | Budget หมด | ใช้ Keyword Matching ก่อน แล้วค่อยเพิ่ม LLM |
| รูปภาพ (Infographic) ขนาดใหญ่ | โหลดช้า | ใช้ CDN หรือ Cloudinary |

---

## 📋 Checklist ก่อนเริ่มพัฒนา

- [ ] ติดตั้ง Docker + Docker Compose
- [ ] ติดตั้ง Python 3.10+
- [ ] สร้าง LINE Official Account
- [ ] ได้ Channel Secret + Access Token
- [ ] สร้าง LIFF App (ได้ LIFF ID)
- [ ] เตรียม Infographic (รูปภาพ)
- [ ] เตรียมเนื้อหา Knowledge + FAQ 33 ข้อ

---

## 📞 การติดต่อและสนับสนุน

| บทบาท | ช่องทาง | หมายเหตุ |
|--------|---------|----------|
| **ผู้ใช้ทั่วไป** | LINE Official Account | แชตกับบอทโดยตรง |
| **ทีมพยาบาล** | Line Message / Phone | รับแจ้งเตือนจากระบบ |
| **Admin** | Django Admin | จัดการข้อมูล, แก้ไขเนื้อหา |
| **Developer** | GitHub Issues | ติดตาม Bug และ Feature |

---

## 📄 เอกสารอ้างอิง

1. [LINE Messaging API Docs](https://developers.line.biz/en/docs/messaging-api/)
2. [LINE LIFF Docs](https://developers.line.biz/en/docs/liff/)
3. [Django Documentation](https://docs.djangoproject.com/)
4. [Celery Documentation](https://docs.celeryq.dev/)
5. [Sepsis Clinical Guidelines](https://www.sepsis.org/)

---

**เอกสารนี้ใช้สำหรับอ้างอิงตลอดการพัฒนา**  
ปรับปรุงล่าสุด: 30 สิงหาคม 2026  
ผู้จัดทำ: วัยรุ่นนน & ทีมพัฒนา 🚀
```

---

# 📄 ไฟล์ที่ 2: `DATABASE_SCHEMA.md`

```markdown
# Sepsis Care Line Chatbot - Database Schema

> PostgreSQL 15+ | Django ORM

---

## 🗂️ ER Diagram (ภาพรวมความสัมพันธ์)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────┐         ┌─────────────┐                                   │
│  │ FamilyGroup │ 1───────*│  LineUser   │                                   │
│  └─────────────┘         └─────────────┘                                   │
│         │                        │                                         │
│         │                        ├───────────┐                             │
│         │                        │           │                             │
│         ▼                        ▼           ▼                             │
│  ┌─────────────┐         ┌────────────┐ ┌─────────────┐                   │
│  │ DailyCheck  │         │VitalSign   │ │SepsisScreening│                   │
│  └─────────────┘         └────────────┘ └─────────────┘                   │
│                                                                             │
│         │                        │                                         │
│         └───────────┬────────────┘                                         │
│                     ▼                                                       │
│              ┌─────────────┐         ┌─────────────┐                       │
│              │Notification │         │   FAQ       │                       │
│              └─────────────┘         └─────────────┘                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────┐               │
│  │                     Knowledge Module                      │               │
│  ├─────────────────────────────────────────────────────────┤               │
│  │  ┌──────────────┐ 1────* ┌──────────────┐ 1────* ┌─────────┐          │
│  │  │ Knowledge    │        │ Knowledge    │        │  Image  │          │
│  │  │ Category     │        │ Article      │        │         │          │
│  │  └──────────────┘        └──────────────┘        └─────────┘          │
│  └─────────────────────────────────────────────────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 รายละเอียดตารางทั้งหมด

### 1. `accounts_familygroup` - กลุ่มครอบครัว

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `code` | VARCHAR(10) | **Unique** รหัสครอบครัว | `FG12345` |
| `created_at` | TIMESTAMP | วันที่สร้าง | 2026-08-30 20:00:00 |

**Index:**
- `code` (Unique Index)

**Validation:**
- `code` ต้องขึ้นต้นด้วย `FG` ตามด้วยเลข 5 หลัก

---

### 2. `accounts_lineuser` - ผู้ใช้ LINE

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `line_user_id` | VARCHAR(50) | **Unique** LINE User ID | `U4af498765...` |
| `display_name` | VARCHAR(100) | ชื่อที่แสดงใน LINE | `สมชาย ใจดี` |
| `name` | VARCHAR(100) | ชื่อ-นามสกุลจริง | `สมชาย ใจดี` |
| `id_card` | VARCHAR(13) | เลขบัตรประชาชน 13 หลัก | `1234567890123` |
| `age` | INTEGER | อายุ | 45 |
| `role` | VARCHAR(10) | บทบาท (`patient` / `caregiver`) | `patient` |
| `family_id` | FK (FamilyGroup) | กลุ่มครอบครัว | 1 |
| `is_registered` | BOOLEAN | ลงทะเบียนแล้วหรือยัง | `True` |
| `registered_at` | TIMESTAMP | วันที่ลงทะเบียน | 2026-08-30 20:00:00 |
| `underlying_disease` | TEXT | โรคประจำตัว (หมอ/พยาบาลเป็นผู้กรอกในระบบ Admin) | `เบาหวาน, ความดัน` |
| `allergy` | TEXT | ประวัติแพ้ยา (เว้นว่างได้) | `Penicillin` |

**Index:**
- `line_user_id` (Unique Index)
- `family_id` (Foreign Key Index)

**Validation:**
- `role` ∈ [`patient`, `caregiver`]
- `id_card` ต้องมีความยาว 13 หลัก (เลขเท่านั้น)
- `age` ต้อง > 0

**Constraint:**
- แต่ละ FamilyGroup ต้องมีผู้ป่วย 1 คน และผู้ดูแล 1 คนเท่านั้น

---

### 3. `assessment_dailycheck` - เช็คอาการรายวัน

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `user_id` | FK (LineUser) | ผู้ที่ตอบแบบประเมิน | 1 |
| `family_id` | FK (FamilyGroup) | กลุ่มครอบครัว | 1 |
| `date` | DATE | วันที่ประเมิน (auto) | 2026-08-30 |
| `has_fever` | BOOLEAN | มีไข้หรือหนาวสั่น? | `True` |
| `fever_detail` | VARCHAR(50) | ระบุอุณหภูมิ (ถ้ามี) | `38.2°C` |
| `has_wound` | BOOLEAN | แผลแดง/บวม/มีน้ำ? | `False` |
| `wound_detail` | VARCHAR(100) | รายละเอียดแผล | - |
| `has_breathless` | BOOLEAN | หายใจเหนื่อยกว่าปกติ? | `False` |
| `breathless_detail` | VARCHAR(100) | รายละเอียดหายใจ | - |
| `has_confused` | BOOLEAN | ซึมหรือสับสนกว่าปกติ? | `False` |
| `confused_detail` | VARCHAR(100) | รายละเอียดอาการ | - |
| `has_less_eat` | BOOLEAN | กิน/ดื่มน้อยลง? | `False` |
| `less_eat_detail` | VARCHAR(100) | รายละเอียด | - |
| `result_level` | VARCHAR(10) | ผลการประเมิน | `green` |
| `responder` | VARCHAR(20) | ผู้ตอบแบบประเมิน | `patient` |
| `responded_at` | TIMESTAMP | เวลาที่ตอบ (auto) | 2026-08-30 09:15:00 |

**Index:**
- `user_id`, `family_id` (FK)
- `date` (สำหรับ Query รายวัน)
- `result_level` (สำหรับกรอง)
- Composite: (`user_id`, `date`) (Unique ต่อวันต่อคน)

**Validation:**
- `result_level` ∈ [`green`, `yellow`, `red`]
- `responder` ∈ [`patient`, `caregiver_help`, `caregiver_replace`]

**Logic:**
```
If all 5 questions = False → green
Elif has_fever OR has_wound OR has_breathless OR has_less_eat → yellow
Elif (has_confused AND (has_fever OR has_breathless OR has_less_eat)) → red
Else → yellow (กรณีอื่นๆ)
```

---

### 4. `assessment_ sepsisscreening` - คัดกรองภาวะเซพซิส

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `user_id` | FK (LineUser) | ผู้ที่ทำแบบประเมิน | 1 |
| `family_id` | FK (FamilyGroup) | กลุ่มครอบครัว | 1 |
| `date` | DATE | วันที่ประเมิน (auto) | 2026-08-30 |

**ปัจจัยเสี่ยง (Risk Factors):**
| `age_over_75` | BOOLEAN | อายุเกิน 75 ปี | `True` |
| `immunocompromised` | BOOLEAN | ภูมิคุ้มกันบกพร่อง | `True` |
| `has_catheter` | BOOLEAN | มีสายสวน/บาดแผล | `False` |
| `recent_surgery` | BOOLEAN | ผ่าตัด/หัตถการล่าสุด | `False` |

**แหล่งติดเชื้อ (Infection Source):**
| `infection_respiratory` | BOOLEAN | ระบบหายใจ | `True` |
| `infection_urinary` | BOOLEAN | ระบบปัสสาวะ | `False` |
| `infection_skin` | BOOLEAN | ผิวหนัง/บาดแผล | `False` |
| `infection_device` | BOOLEAN | วัตถุค้างในร่างกาย | `False` |
| `infection_brain` | BOOLEAN | สมอง | `False` |
| `infection_surgery` | BOOLEAN | การผ่าตัด | `False` |
| `infection_other` | VARCHAR(200) | อื่นๆ (ระบุ) | - |

**Red Flags (7 อาการรุนแรง):**
| `red_flag_mental` | BOOLEAN | สภาพจิตใจเปลี่ยนแปลง | `False` |
| `red_flag_rr_ge25` | BOOLEAN | RR ≥ 25 ครั้ง/นาที | `False` |
| `red_flag_o2_need` | BOOLEAN | ต้องให้ O2 ≥ 40% | `False` |
| `red_flag_sbp_le90` | BOOLEAN | SBP ≤ 90 mmHg | `False` |
| `red_flag_hr_gt130` | BOOLEAN | HR > 130 ครั้ง/นาที | `False` |
| `red_flag_no_urine_18h` | BOOLEAN | ไม่ปัสสาวะ 18 ชม. | `False` |
| `red_flag_skin_change` | BOOLEAN | ผิวหนังเปลี่ยนสี | `False` |

**Amber Flags (10 อาการเฝ้าระวัง):**
| `amber_flag_behavior` | BOOLEAN | พฤติกรรมผิดปกติ | `False` |
| `amber_flag_activity_down` | BOOLEAN | กิจกรรมลดลง | `False` |
| `amber_flag_rr_21_24` | BOOLEAN | RR 21-24 ครั้ง/นาที | `False` |
| `amber_flag_sbp_91_100` | BOOLEAN | SBP 91-100 mmHg | `False` |
| `amber_flag_hr_91_120` | BOOLEAN | HR 91-120 ครั้ง/นาที | `False` |
| `amber_flag_spo2_lt92` | BOOLEAN | SpO₂ < 92% | `False` |
| `amber_flag_no_urine_12_18h` | BOOLEAN | ไม่ปัสสาวะ 12-18 ชม. | `False` |
| `amber_flag_immuno` | BOOLEAN | ภูมิคุ้มกันบกพร่อง | `False` |
| `amber_flag_infection_sign` | BOOLEAN | สัญญาณติดเชื้อ | `False` |
| `amber_flag_temp_lt36` | BOOLEAN | Temp < 36°C | `False` |

**สรุปผล:**
| `has_red_flag` | BOOLEAN | พบ Red Flag อย่างน้อย 1 ข้อ | `False` |
| `has_amber_flag` | BOOLEAN | พบ Amber Flag อย่างน้อย 1 ข้อ | `True` |
| `result` | TEXT | คำแนะนำตามผล | `"พบ Amber Flag ควร..."` |

**Index:**
- `user_id`, `family_id` (FK)
- `date` (Query ตามวันที่)
- `has_red_flag`, `has_amber_flag` (กรอง)

---

### 5. `health_vitalsign` - บันทึกสัญญาณชีพ

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `user_id` | FK (LineUser) | ผู้ป่วย | 1 |
| `family_id` | FK (FamilyGroup) | กลุ่มครอบครัว | 1 |
| `date` | DATE | วันที่บันทึก (auto) | 2026-08-30 |
| `temperature` | FLOAT | อุณหภูมิ (°C) | 36.8 |
| `heart_rate` | INTEGER | ชีพจร (ครั้ง/นาที) | 76 |
| `systolic_bp` | INTEGER | ความดันตัวบน (mmHg) | 120 |
| `diastolic_bp` | INTEGER | ความดันตัวล่าง (mmHg) | 80 |
| `respiratory_rate` | INTEGER | อัตราการหายใจ (ครั้ง/นาที) | 16 |
| `spo2` | INTEGER | SpO₂ (%) | 98 |
| `recorded_at` | TIMESTAMP | เวลาที่บันทึก (auto) | 2026-08-30 14:30:00 |

**Index:**
- `user_id`, `family_id` (FK)
- `date` (Query วันที่ 14 และ 30)

**Validation:**
- `temperature`: 35.0 - 42.0°C
- `heart_rate`: 30 - 250
- `systolic_bp`: 60 - 250
- `diastolic_bp`: 30 - 200
- `respiratory_rate`: 5 - 60
- `spo2`: 70 - 100

---

### 6. `knowledge_knowledgecategory` - หมวดหมู่ความรู้

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `name` | VARCHAR(100) | ชื่อหมวดหมู่ | `การดูแลตนเอง` |
| `slug` | VARCHAR(100) | **Unique** URL-friendly | `self-care` |
| `icon` | VARCHAR(50) | Emoji หรือ CSS class | `🩺` |
| `order` | INTEGER | ลำดับการแสดง | 1 |

**Index:**
- `slug` (Unique)

**Seed Data:**
1. `การดูแลตนเอง` (self-care, 🏠)
2. `ความรู้เซพซิส` (sepsis-edu, 📖)
3. `การฟื้นฟู` (recovery, 💪)
4. `การป้องกัน` (prevention, 🛡️)

---

### 7. `knowledge_knowledgearticle` - บทความความรู้

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `category_id` | FK (KnowledgeCategory) | หมวดหมู่ | 1 |
| `title` | VARCHAR(200) | ชื่อบทความ | `การดูแลแผลหลังผ่าตัด` |
| `content` | TEXT | เนื้อหา (HTML) | `<p>...</p>` |
| `summary` | TEXT | ข้อความสั้นๆ (Preview) | `รักษาแผลให้สะอาด...` |
| `is_published` | BOOLEAN | เผยแพร่แล้ว? | `True` |
| `send_schedule` | VARCHAR(20) | ตารางส่งอัตโนมัติ | `mon_thu` |
| `created_at` | TIMESTAMP | วันที่สร้าง (auto) | 2026-08-30 |
| `updated_at` | TIMESTAMP | วันที่แก้ไข (auto) | 2026-08-30 |

**Index:**
- `category_id` (FK)
- `is_published` (Filter)
- `send_schedule` (สำหรับ Scheduler)

**Validation:**
- `send_schedule` ∈ [``, `mon_thu`, `custom`]

---

### 8. `knowledge_image` - รูปภาพ (Gallery)

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `article_id` | FK (KnowledgeArticle) | บทความที่เกี่ยวข้อง | 1 |
| `image` | ImageField | ไฟล์รูปภาพ | `gallery/1_infographic.jpg` |
| `caption` | VARCHAR(200) | คำอธิบายใต้รูป | `รูปแสดงอาการ Sepsis` |
| `order` | INTEGER | ลำดับรูป (0 = แรก) | 0 |

**Index:**
- `article_id` (FK)
- `order` (เรียงลำดับ)

**Storage:**
- เก็บใน `media/gallery/`
- ขนาดแนะนำ: < 5MB ต่อรูป
- Format: JPEG, PNG, WebP

---

### 9. `faq_faq` - คำถามที่พบบ่อย (33 ข้อ)

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `question` | VARCHAR(200) | คำถาม | `ภาวะเซพซิสคืออะไร?` |
| `answer` | TEXT | คำตอบ | `ภาวะเซพซิสคือ...` |
| `order` | INTEGER | ลำดับ (Sort) | 1 |
| `category` | VARCHAR(50) | หมวดหมู่ (Optional) | `general` |

**Index:**
- `order` (เรียง)
- `category` (Filter)

**Validation:**
- `category` ∈ [`general`, `medication`, `emergency`, `recovery`]

---

### 10. `notification_notificationlog` - บันทึกการแจ้งเตือน

| Field | Type | คำอธิบาย | ตัวอย่าง |
|-------|------|----------|----------|
| `id` | SERIAL | Primary Key | 1 |
| `user_id` | FK (LineUser) | ผู้รับ | 1 |
| `family_id` | FK (FamilyGroup) | กลุ่มครอบครัว | 1 |
| `type` | VARCHAR(20) | ประเภทการแจ้งเตือน | `daily_check` |
| `message` | TEXT | ข้อความที่ส่ง | `กรุณาเช็คอาการ...` |
| `is_sent` | BOOLEAN | ส่งแล้วหรือยัง | `True` |
| `sent_at` | TIMESTAMP | เวลาที่ส่ง | 2026-08-30 09:00:00 |
| `created_at` | TIMESTAMP | วันที่สร้าง (auto) | 2026-08-30 |

**Index:**
- `user_id`, `family_id` (FK)
- `is_sent` (Query ยังไม่ส่ง)
- `type` (กรองประเภท)
- `created_at` (Query ตามวันที่)

**Validation:**
- `type` ∈ [`daily_check`, `sepsis_edu`, `non_response`, `emergency`]

---

## 🔗 Foreign Key Relationships (FK)

| Table | FK Field | References | On Delete |
|-------|----------|------------|-----------|
| `LineUser` | `family_id` | `FamilyGroup.id` | CASCADE |
| `DailyCheck` | `user_id` | `LineUser.id` | CASCADE |
| `DailyCheck` | `family_id` | `FamilyGroup.id` | CASCADE |
| `SepsisScreening` | `user_id` | `LineUser.id` | CASCADE |
| `SepsisScreening` | `family_id` | `FamilyGroup.id` | CASCADE |
| `VitalSign` | `user_id` | `LineUser.id` | CASCADE |
| `VitalSign` | `family_id` | `FamilyGroup.id` | CASCADE |
| `KnowledgeArticle` | `category_id` | `KnowledgeCategory.id` | CASCADE |
| `Image` | `article_id` | `KnowledgeArticle.id` | CASCADE |
| `NotificationLog` | `user_id` | `LineUser.id` | CASCADE |
| `NotificationLog` | `family_id` | `FamilyGroup.id` | CASCADE |

---

## 📊 Index Summary (เพื่อประสิทธิภาพ)

| Table | Index | Type | คำอธิบาย |
|-------|-------|------|----------|
| `FamilyGroup` | `code` | UNIQUE | ค้นหาด้วยรหัส |
| `LineUser` | `line_user_id` | UNIQUE | ค้นหาผู้ใช้จาก LINE |
| `LineUser` | `family_id` | INDEX | JOIN กับ FamilyGroup |
| `DailyCheck` | (`user_id`, `date`) | UNIQUE | ป้องกันการกรอกซ้ำต่อวัน |
| `DailyCheck` | `result_level` | INDEX | กรองสีเขียว/เหลือง/แดง |
| `SepsisScreening` | (`user_id`, `date`) | INDEX | ดึงประวัติผู้ใช้ |
| `VitalSign` | (`user_id`, `date`) | INDEX | ดึงวันที่ 14 และ 30 |
| `KnowledgeArticle` | `category_id` | INDEX | JOIN หมวดหมู่ |
| `KnowledgeArticle` | `is_published` | INDEX | กรองบทความที่เผยแพร่ |
| `NotificationLog` | `is_sent` | INDEX | ดึงที่ยังไม่ได้ส่ง |
| `NotificationLog` | `created_at` | INDEX | Query ตามวันที่ |

---

## 🗄️ SQL Script (Migration เริ่มต้น)

```sql
-- 1. FamilyGroup
CREATE TABLE accounts_familygroup (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. LineUser
CREATE TABLE accounts_lineuser (
    id SERIAL PRIMARY KEY,
    line_user_id VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    id_card VARCHAR(13) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0),
    role VARCHAR(10) NOT NULL CHECK (role IN ('patient', 'caregiver')),
    family_id INTEGER REFERENCES accounts_familygroup(id) ON DELETE CASCADE,
    is_registered BOOLEAN DEFAULT FALSE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    underlying_disease TEXT,
    allergy TEXT
);

-- 3. DailyCheck
CREATE TABLE assessment_dailycheck (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_lineuser(id) ON DELETE CASCADE,
    family_id INTEGER REFERENCES accounts_familygroup(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    has_fever BOOLEAN DEFAULT FALSE,
    fever_detail VARCHAR(50),
    has_wound BOOLEAN DEFAULT FALSE,
    wound_detail VARCHAR(100),
    has_breathless BOOLEAN DEFAULT FALSE,
    breathless_detail VARCHAR(100),
    has_confused BOOLEAN DEFAULT FALSE,
    confused_detail VARCHAR(100),
    has_less_eat BOOLEAN DEFAULT FALSE,
    less_eat_detail VARCHAR(100),
    result_level VARCHAR(10) CHECK (result_level IN ('green', 'yellow', 'red')),
    responder VARCHAR(20) CHECK (responder IN ('patient', 'caregiver_help', 'caregiver_replace')),
    responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);

-- 4. SepsisScreening
CREATE TABLE assessment_sepsisscreening (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_lineuser(id) ON DELETE CASCADE,
    family_id INTEGER REFERENCES accounts_familygroup(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    age_over_75 BOOLEAN DEFAULT FALSE,
    immunocompromised BOOLEAN DEFAULT FALSE,
    has_catheter BOOLEAN DEFAULT FALSE,
    recent_surgery BOOLEAN DEFAULT FALSE,
    infection_respiratory BOOLEAN DEFAULT FALSE,
    infection_urinary BOOLEAN DEFAULT FALSE,
    infection_skin BOOLEAN DEFAULT FALSE,
    infection_device BOOLEAN DEFAULT FALSE,
    infection_brain BOOLEAN DEFAULT FALSE,
    infection_surgery BOOLEAN DEFAULT FALSE,
    infection_other VARCHAR(200),
    red_flag_mental BOOLEAN DEFAULT FALSE,
    red_flag_rr_ge25 BOOLEAN DEFAULT FALSE,
    red_flag_o2_need BOOLEAN DEFAULT FALSE,
    red_flag_sbp_le90 BOOLEAN DEFAULT FALSE,
    red_flag_hr_gt130 BOOLEAN DEFAULT FALSE,
    red_flag_no_urine_18h BOOLEAN DEFAULT FALSE,
    red_flag_skin_change BOOLEAN DEFAULT FALSE,
    amber_flag_behavior BOOLEAN DEFAULT FALSE,
    amber_flag_activity_down BOOLEAN DEFAULT FALSE,
    amber_flag_rr_21_24 BOOLEAN DEFAULT FALSE,
    amber_flag_sbp_91_100 BOOLEAN DEFAULT FALSE,
    amber_flag_hr_91_120 BOOLEAN DEFAULT FALSE,
    amber_flag_spo2_lt92 BOOLEAN DEFAULT FALSE,
    amber_flag_no_urine_12_18h BOOLEAN DEFAULT FALSE,
    amber_flag_immuno BOOLEAN DEFAULT FALSE,
    amber_flag_infection_sign BOOLEAN DEFAULT FALSE,
    amber_flag_temp_lt36 BOOLEAN DEFAULT FALSE,
    has_red_flag BOOLEAN DEFAULT FALSE,
    has_amber_flag BOOLEAN DEFAULT FALSE,
    result TEXT
);

-- 5. VitalSign
CREATE TABLE health_vitalsign (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_lineuser(id) ON DELETE CASCADE,
    family_id INTEGER REFERENCES accounts_familygroup(id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    temperature FLOAT,
    heart_rate INTEGER,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    respiratory_rate INTEGER,
    spo2 INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. KnowledgeCategory
CREATE TABLE knowledge_knowledgecategory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50),
    order INTEGER DEFAULT 0
);

-- 7. KnowledgeArticle
CREATE TABLE knowledge_knowledgearticle (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES knowledge_knowledgecategory(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    is_published BOOLEAN DEFAULT TRUE,
    send_schedule VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Image
CREATE TABLE knowledge_image (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES knowledge_knowledgearticle(id) ON DELETE CASCADE,
    image VARCHAR(200) NOT NULL,
    caption VARCHAR(200),
    order INTEGER DEFAULT 0
);

-- 9. FAQ
CREATE TABLE faq_faq (
    id SERIAL PRIMARY KEY,
    question VARCHAR(200) NOT NULL,
    answer TEXT NOT NULL,
    order INTEGER DEFAULT 0,
    category VARCHAR(50)
);

-- 10. NotificationLog
CREATE TABLE notification_notificationlog (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_lineuser(id) ON DELETE CASCADE,
    family_id INTEGER REFERENCES accounts_familygroup(id) ON DELETE CASCADE,
    type VARCHAR(20) CHECK (type IN ('daily_check', 'sepsis_edu', 'non_response', 'emergency')),
    message TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Create Indexes
CREATE INDEX idx_lineuser_family ON accounts_lineuser(family_id);
CREATE INDEX idx_dailycheck_user_date ON assessment_dailycheck(user_id, date);
CREATE INDEX idx_dailycheck_result ON assessment_dailycheck(result_level);
CREATE INDEX idx_sepsisscreening_user_date ON assessment_sepsisscreening(user_id, date);
CREATE INDEX idx_vitalsign_user_date ON health_vitalsign(user_id, date);
CREATE INDEX idx_article_category ON knowledge_knowledgearticle(category_id);
CREATE INDEX idx_article_published ON knowledge_knowledgearticle(is_published);
CREATE INDEX idx_image_article ON knowledge_image(article_id);
CREATE INDEX idx_notification_sent ON notification_notificationlog(is_sent);
CREATE INDEX idx_notification_created ON notification_notificationlog(created_at);
```

---

## 🔄 Migration Command

```bash
# สร้าง migrations
python manage.py makemigrations accounts
python manage.py makemigrations assessment
python manage.py makemigrations health
python manage.py makemigrations knowledge
python manage.py makemigrations faq
python manage.py makemigrations notification

# Apply migrations
python manage.py migrate

# ตรวจสอบตารางในฐานข้อมูล
python manage.py dbshell
\dt
```

---

## 🧪 Seed Data (ข้อมูลเริ่มต้น)

### FAQ 33 ข้อ
```python
# scripts/seed_faq.py
FAQ.objects.bulk_create([
    FAQ(question="ภาวะเซพซิสคืออะไร?", answer="...", order=1, category="general"),
    # ... 33 ข้อ
])
```

### Knowledge Categories
```python
# scripts/seed_categories.py
categories = [
    {"name": "การดูแลตนเอง", "slug": "self-care", "icon": "🏠"},
    {"name": "ความรู้เซพซิส", "slug": "sepsis-edu", "icon": "📖"},
    {"name": "การฟื้นฟู", "slug": "recovery", "icon": "💪"},
    {"name": "การป้องกัน", "slug": "prevention", "icon": "🛡️"},
]
```

---

## 📈 Performance Tips

1. **Use Indexes** - สร้าง index บน foreign key และ field ที่ใช้ query บ่อย
2. **JSON Field** - ถ้าข้อมูลยืดหยุ่นสูง ใช้ `JSONField` แทนการเพิ่ม column
3. **Query Optimization** - ใช้ `select_related()` และ `prefetch_related()` ใน Django
4. **Partitioning** - ถ้ามีข้อมูลมาก → Partition Table รายเดือน (DailyCheck, NotificationLog)
5. **Read Replica** - สำหรับ Dashboard และ Report (แยกจาก Transaction)

---

## 🗂️ เอกสารนี้ใช้สำหรับอ้างอิงตลอดการพัฒนา

**ปรับปรุงล่าสุด:** 30 สิงหาคม 2026  
**ผู้จัดทำ:** วัยรุ่นนน & ทีมพัฒนา 🚀

---

**พร้อมเริ่มโค้ดแล้วครับ!** บอกได้เลยว่าอยากให้ช่วยทำส่วนไหนต่อ 🙌
```

---

## 📝 สรุป

ผมได้จัดทำเอกสาร 2 ไฟล์ให้คุณแล้วครับ:

1. **`PROJECT_OVERVIEW.md`** - ครอบคลุม:
   - ภาพรวมโครงการ
   - สถาปัตยกรรมระบบ
   - Flow การทำงาน
   - Tech Stack
   - โครงสร้างโปรเจกต์
   - Roadmap การพัฒนา
   - ความเสี่ยงและแนวทางแก้ไข

2. **`DATABASE_SCHEMA.md`** - ครอบคลุม:
   - ER Diagram
   - รายละเอียดทุกตาราง (10 ตาราง)
   - Field, Type, คำอธิบาย, ตัวอย่าง
   - Foreign Key Relationships
   - Indexes
   - SQL Script เต็มรูปแบบ
   - Seed Data
   - Performance Tips

---

**ถามเพิ่มได้เลยครับ!** 
- อยากปรับแก้ตรงไหน?
- อยากให้ขยายความส่วนไหน?
- อยากให้ช่วยเขียน Models จริงเป็น Django Code?

**บอกมาเลยครับ พร้อมลุยคืนนี้!** 🚀🔥