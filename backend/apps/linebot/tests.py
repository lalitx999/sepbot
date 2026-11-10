from django.test import SimpleTestCase

from .llm_service import to_plain_text


class ToPlainTextTests(SimpleTestCase):
    def test_strips_markdown_from_real_reply(self):
        raw = (
            "**สรุปภาพ**\n- ไม่มีไข้\n- มีน้ำมูกและเจ็บคอ\n\n---\n\n"
            "## 1. การดูแลตนเองที่บ้าน\n\n"
            "| # | สิ่งที่ทำ | คำอธิบาย |\n|---|-----------|-----------|\n"
            "| 1 | **พักผ่อนให้เพียงพอ** | นอน 7–8 ชม./คืน |\n"
            "| 2 | **ดื่มน้ำให้เพียงพอ** | ดื่ม 1.5–2 ลิตรต่อวัน |\n"
        )
        out = to_plain_text(raw)
        for ch in ('*', '|', '#', '---'):
            self.assertNotIn(ch, out)
        self.assertIn('สรุปภาพ', out)
        self.assertIn('• ไม่มีไข้', out)
        self.assertIn('1. การดูแลตนเองที่บ้าน', out)
        self.assertIn('• พักผ่อนให้เพียงพอ – นอน 7–8 ชม./คืน', out)
        self.assertNotIn('สิ่งที่ทำ', out)  # table header row dropped

    def test_plain_text_unchanged(self):
        text = "สวัสดีค่ะ\n1. ดื่มน้ำ\n2. พักผ่อน"
        self.assertEqual(to_plain_text(text), text)

    def test_dangling_marks_and_empty(self):
        self.assertEqual(to_plain_text("- **อย่า"), "• อย่า")
        self.assertEqual(to_plain_text(""), "")
        self.assertEqual(to_plain_text(None), "")
