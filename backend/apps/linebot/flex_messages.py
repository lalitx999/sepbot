import os

def build_greeting_flex(display_name=""):
    """
    Flex Message sent on initial Add LINE / Greeting.
    Contains button to open LIFF registration with personalized welcome text.
    """
    liff_register_url = f"https://liff.line.me/{os.getenv('LINE_LIFF_ID_REGISTER', 'demo_register')}"
    name_text = f"สวัสดีคุณ {display_name}" if display_name else "สวัสดีค่ะ"

    return {
        "type": "flex",
        "altText": "ยินดีต้อนรับสู่ Sepsis Care Line - กรุณาลงทะเบียน",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Sepsis Care",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "lg",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#2E7D32",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": name_text,
                        "weight": "bold",
                        "size": "md",
                        "color": "#2E7D32",
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": "ขอบคุณที่เป็นเพื่อนกับเราค่ะ 💚\nนี่คือระบบบริการติดตามและดูแลผู้ป่วยภาวะเซพซิส (Sepsis Care)\n\nเพื่อเริ่มใช้งานระบบและติดตามสุขภาพอย่างปลอดภัย กรุณากดปุ่มด้านล่างเพื่อลงทะเบียนและผูกครอบครัวนะคะ",
                        "wrap": True,
                        "size": "sm",
                        "color": "#444444",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "📝 ลงทะเบียนเพื่อเริ่มใช้งาน",
                            "uri": liff_register_url
                        },
                        "style": "primary",
                        "color": "#2E7D32"
                    }
                ]
            }
        }
    }


def build_emergency_contacts_flex():
    """
    Flex Message sent when user clicks Emergency contact in Rich Menu.
    Ordered as:
    1) ผู้วิจัย ณัฏฐณิชา สิงห์จาน
    2) สายด่วนการแพทย์ฉุกเฉิน 1669
    3) โรงพยาบาลใกล้บ้าน
    4) รพ.จุฬาลงกรณ์ 022564000
    """
    emergency_phone = os.getenv('EMERGENCY_PHONE_1669', '1669')
    hospital_phone = os.getenv('HOSPITAL_CHULA_PHONE', '022564000')
    nurse_phone = os.getenv('NURSE_CONTACT_PHONE', '0996244555')

    return {
        "type": "flex",
        "altText": "🚨 ช่องทางติดต่อฉุกเฉิน",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🚨 ช่องทางติดต่อฉุกเฉิน",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#D32F2F",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "กรุณาเลือกช่องทางติดต่อด้านล่างทันที:",
                        "weight": "bold",
                        "color": "#D32F2F",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "หากมีอาการทรุดลงหรือสงสัยภาวะติดเชื้อในกระแสเลือด กรุณาติดต่อผู้วิจัยหรือโทร 1669 ทันที",
                        "wrap": True,
                        "size": "xs",
                        "color": "#555555",
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "1) ผู้วิจัย ณัฏฐณิชา สิงห์จาน",
                            "uri": f"tel:{nurse_phone}"
                        },
                        "style": "primary",
                        "color": "#7B3F9E"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "2) สายด่วนการแพทย์ฉุกเฉิน 1669",
                            "uri": f"tel:{emergency_phone}"
                        },
                        "style": "primary",
                        "color": "#D32F2F"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "3) โรงพยาบาลใกล้บ้าน",
                            "uri": "https://www.google.com/maps/search/โรงพยาบาลใกล้ฉัน"
                        },
                        "style": "secondary"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "4) รพ.จุฬาลงกรณ์ 022564000",
                            "uri": f"tel:{hospital_phone}"
                        },
                        "style": "secondary"
                    }
                ]
            }
        }
    }


def build_emergency_flex():
    """
    Flex Message sent when user clicks Emergency contact in Rich Menu.
    Displays emergency infographic image and direct 1669 call button below.
    """
    base_url = os.getenv('BASE_URL', 'https://app11.tanchonhomserverxxx.online').rstrip('/')
    emergency_phone = os.getenv('EMERGENCY_PHONE_1669', '1669')
    img_url = f"{base_url}/media/infographics/emergency_contact.jpg"

    return {
        "type": "flex",
        "altText": "🚨 ติดต่อฉุกเฉิน 1669",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": img_url,
                "size": "full",
                "aspectRatio": "682:1024",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": img_url
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "หากมีอาการทรุดลงหรือสงสัยภาวะเซพซิส กรุณาติดต่อผู้วิจัยหรือโทร 1669 ทันที",
                        "wrap": True,
                        "weight": "bold",
                        "size": "sm",
                        "color": "#D32F2F"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "📞 โทร 1669 ทันที",
                            "uri": f"tel:{emergency_phone}"
                        },
                        "style": "primary",
                        "color": "#D32F2F"
                    }
                ]
            }
        }
    }


def build_emergency_symptoms_info_flex():
    """
    Flex Message displaying Red Flag Emergency symptoms infographic details.
    """
    return {
        "type": "flex",
        "altText": "🚨 ข้อมูลอาการฉุกเฉินสีแดง (Red Flags)",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ สัญญาณอันตรายฉุกเฉิน (สีแดง)",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "md"
                    }
                ],
                "backgroundColor": "#C62828",
                "paddingAll": "12px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "หากมีอาการข้อใดข้อหนึ่งดังนี้ ให้รีบพบแพทย์ด่วน:",
                        "weight": "bold",
                        "color": "#C62828",
                        "size": "xs",
                        "margin": "none"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "text",
                                "text": "• ซึมมาก ไม่รู้สึกตัว หรือสับสนเฉียบพลัน",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• หายใจเร็ว หอบเหนื่อย หรือหายใจลำบากมาก",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• หัวใจเต้นเร็วผิดปกติ (> 130 ครั้ง/นาที)",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• ความดันโลหิตตก (ตัวบน ≤ 90 mmHg)",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• ไม่มีปัสสาวะออกเลยตลอดทั้งวัน (> 18 ชม.)",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• ผิวหนังลายด่าง ลายลูกหิน หรือเขียวคล้ำ",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• แผลติดเชื้อ บวม แดง ร้อน มีหนอง ลุกลาม",
                                "size": "xs",
                                "color": "#333333",
                                "wrap": True
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "📞 โทร 1669 ทันที",
                            "uri": "tel:1669"
                        },
                        "style": "primary",
                        "color": "#D32F2F"
                    }
                ]
            }
        }
    }


def build_default_help_flex():
    """
    Fallback Flex Message when text is not understood or user needs help.
    """
    return {
        "type": "flex",
        "altText": "SepCare AI พร้อมช่วยเหลือค่ะ",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "SepCare AI",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "ผู้ช่วยดูแลสุขภาพและการฟื้นฟูหลังภาวะเซพซิส",
                        "color": "#E0F2F1",
                        "size": "xs",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": "#00897B",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "สามารถพิมพ์สอบถามคำถามด้านสุขภาพและการดูแลตนเองกับ SepCare AI ได้เลยนะคะ 💙",
                        "wrap": True,
                        "size": "sm",
                        "color": "#333333",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "หรือกดเลือกดูคำถามยอดนิยมที่พบบ่อย (33 ข้อ) จากปุ่มด้านล่างได้ค่ะ",
                        "wrap": True,
                        "size": "xs",
                        "color": "#666666",
                        "margin": "md"
                    }
                ],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "📚 ดูคำถามยอดนิยม (33 ข้อ)",
                            "text": "__SHOW_ALL_QUESTIONS__"
                        },
                        "style": "primary",
                        "color": "#00897B",
                        "height": "sm"
                    }
                ]
            }
        }
    }


def build_ask_nurse_flex():
    """
    Flex Message sent when user clicks "ถามพยาบาล" on Rich Menu or types "ถามพยาบาล".
    Provides direct contact to research project nurse via LINE chat or phone.
    """
    nurse_line_link = os.getenv('NURSE_LINE_PERSONAL_LINK', 'https://line.me/ti/p/~Siine8')
    nurse_phone = os.getenv('NURSE_CONTACT_PHONE', '0996244555')

    return {
        "type": "flex",
        "altText": "💬 สอบถามพยาบาลโครงการ",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💬 สอบถามพยาบาลโครงการ",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#7B3F9E",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "หากมีข้อสงสัยหรือต้องการคำปรึกษาเพิ่มเติมเกี่ยวกับการดูแลผู้ป่วย สามารถกดปุ่มด้านล่างเพื่อพูดคุยหรือโทรติดต่อพยาบาลโครงการโดยตรงได้เลยค่ะ 💙",
                        "wrap": True,
                        "size": "sm",
                        "color": "#444444"
                    }
                ],
                "paddingAll": "16px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "💬 แชทกับพยาบาลโครงการ",
                            "uri": nurse_line_link
                        },
                        "style": "primary",
                        "color": "#7B3F9E"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": f"📞 โทรหาพยาบาล ({nurse_phone})",
                            "uri": f"tel:{nurse_phone}"
                        },
                        "style": "secondary"
                    }
                ]
            }
        }
    }


def build_ai_response_flex(ai_answer, user_question=None):
    """
    Flex Message Card for SepCare AI responses.
    Clean medical teal banner theme.
    Displays only the AI answer in the card body.
    """
    return {
        "type": "flex",
        "altText": "SepCare AI: คำแนะนำการดูแลสุขภาพ",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "SepCare AI - คำแนะนำการดูแลสุขภาพ",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "md"
                    }
                ],
                "backgroundColor": "#005B5C",
                "paddingAll": "12px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": ai_answer,
                        "wrap": True,
                        "size": "sm",
                        "color": "#333333"
                    }
                ]
            }
        }
    }


def build_ebook_flex():
    """
    Flex Message Card for opening SepCare Interactive E-Book.
    """
    base_url = os.getenv('BASE_URL', 'https://app11.tanchonhomserverxxx.online').rstrip('/')
    ebook_url = f"{base_url}/ebook/"

    return {
        "type": "flex",
        "altText": "📖 SepCare E-book คู่มือการจัดการตนเองสำหรับผู้ป่วยสูงอายุหลังภาวะเซพซิส",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "E-book คู่มือการจัดการตนเองสำหรับผู้ป่วยสูงอายุหลังภาวะเซพซิส",
                        "wrap": True,
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#0B69A3",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "E-book คู่มือการจัดการตนเองสำหรับผู้ป่วยสูงอายุหลังภาวะเซพซิส",
                        "wrap": True,
                        "weight": "bold",
                        "size": "sm",
                        "color": "#0B69A3"
                    },
                    {
                        "type": "text",
                        "text": "เปิดอ่านเสมือนเปิดหนังสือจริง พลิกหน้าได้ทั้งบนมือถือและคอมพิวเตอร์ รวม 48 หน้า พร้อมภาพอินโฟกราฟิกและสารบัญแยกตามบท",
                        "wrap": True,
                        "size": "xs",
                        "color": "#555555",
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "📖 เปิดอ่าน E-Book ตอนนี้",
                            "uri": ebook_url
                        },
                        "style": "primary",
                        "color": "#0B69A3"
                    }
                ]
            }
        }
    }


def build_greeting_chat_flex(display_name=""):
    """Flex Message สำหรับ greeting (ทักทายในแชท)"""
    name_text = f"สวัสดีคุณ {display_name} 🙏" if display_name else "สวัสดีค่ะ 🙏"

    return {
        "type": "flex",
        "altText": "สวัสดีค่ะ SepCare AI พร้อมช่วยเหลือ",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "SepCare AI", "weight": "bold", "color": "#FFFFFF", "size": "lg"},
                    {"type": "text", "text": "ผู้ช่วยดูแลผู้ป่วยหลังภาวะเซพซิส", "color": "#E0F2F1", "size": "xs", "margin": "xs"}
                ],
                "backgroundColor": "#00897B",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": name_text, "weight": "bold", "size": "md", "color": "#00897B", "wrap": True},
                    {"type": "text", "text": "ยินดีให้คำปรึกษาเรื่องการดูแลสุขภาพและการดูแลผู้ป่วยหลังภาวะเซพซิสค่ะ 💙", "size": "sm", "color": "#444444", "wrap": True, "margin": "md"},
                    {"type": "separator", "margin": "lg"},
                    {"type": "text", "text": "ตัวอย่างคำถามที่สอบถามได้:", "weight": "bold", "size": "sm", "color": "#00897B", "margin": "lg"},
                    {"type": "text", "text": "• ภาวะเซพซิสคืออะไร", "size": "sm", "color": "#333333", "wrap": True, "margin": "md"},
                    {"type": "text", "text": "• ควรตรวจสัญญาณชีพอะไรทุกวัน", "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• การดูแลแผลและสายสวนปัสสาวะ", "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• ลืมกินยาตามเวลาควรทำอย่างไร", "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"}
                ],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "💬 ตัวอย่าง: ควรตรวจอะไรทุกวัน", "text": "ควรตรวจอะไรทุกวัน"},
                        "style": "primary", "color": "#00897B", "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "📚 ดูคำถามยอดนิยม (33 ข้อ)", "text": "__SHOW_ALL_QUESTIONS__"},
                        "style": "secondary", "height": "sm"
                    }
                ]
            }
        }
    }


def build_all_questions_flex():
    """Flex Message แสดงรายการคำถามทั้งหมด 33 ข้อ (carousel 4 กลุ่ม)"""
    group1 = {
        "type": "bubble", "size": "kilo",
        "header": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "🩺 อาการและความเสี่ยง", "weight": "bold", "color": "#FFFFFF", "size": "md"}],
            "backgroundColor": "#00897B", "paddingAll": "12px"
        },
        "body": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "1. ภาวะเซพซิสคืออะไร", "text": "ภาวะเซพซิสคืออะไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "2. เป็นซ้ำได้ไหม", "text": "หลังออกจากโรงพยาบาล ยังมีโอกาสเกิดเซพซิสซ้ำหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "3. ฟื้นตัวนานไหม", "text": "ต้องใช้เวลานานเท่าใดจึงจะฟื้นตัว"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "4. อาการที่พบบ่อย", "text": "อาการหลังภาวะเซพซิสที่พบบ่อยมีอะไรบ้าง"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "9. ไม่มีไข้ = ไม่ติดเชื้อ?", "text": "ถ้าไม่มีไข้ แสดงว่าไม่มีการติดเชื้อใช่หรือไม่"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "12px"
        }
    }

    group2 = {
        "type": "bubble", "size": "kilo",
        "header": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "🌡️ การติดตามอาการ", "weight": "bold", "color": "#FFFFFF", "size": "md"}],
            "backgroundColor": "#0277BD", "paddingAll": "12px"
        },
        "body": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "5. ตรวจอะไรทุกวัน", "text": "ควรตรวจอะไรทุกวัน"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "6. อุณหภูมิเท่าไหร่แจ้ง", "text": "อุณหภูมิเท่าใดควรแจ้งพยาบาล"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "7. เมื่อไหร่ติดต่อหน่วยบริการ", "text": "เมื่อใดควรติดต่อหน่วยบริการสุขภาพ"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🚨 8. อาการไหนโทร 1669", "text": "อาการใดต้องโทร 1669 ทันที"}, "style": "primary", "color": "#D32F2F", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "22. วัดออกซิเจนปลายนิ้ว", "text": "ควรวัดค่าออกซิเจนปลายนิ้วหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "23. ปัสสาวะน้อยลง", "text": "ปัสสาวะน้อยลงควรทำอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "24. ติดเชื้อทางเดินปัสสาวะ", "text": "อาการใดอาจบ่งชี้การติดเชื้อทางเดินปัสสาวะ"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "32. ติดตามอาการหลังออก รพ.", "text": "หลังออกจากโรงพยาบาล ควรติดตามอาการอะไรบ้าง"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "12px"
        }
    }

    group3 = {
        "type": "bubble", "size": "kilo",
        "header": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "💊 ยาและการรักษา", "weight": "bold", "color": "#FFFFFF", "size": "md"}],
            "backgroundColor": "#7B3F9E", "paddingAll": "12px"
        },
        "body": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "10. ดูแลบาดแผล", "text": "ควรดูแลบาดแผลอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "13. ใช้ยาปฏิชีวนะ", "text": "ควรใช้ยาปฏิชีวนะอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "14. ลืมกินยา", "text": "ถ้าลืมรับประทานยาควรทำอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "15. ป้องกันการติดเชื้อซ้ำ", "text": "ป้องกันการติดเชื้อซ้ำได้อย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "16. ไปพบแพทย์ตามนัด", "text": "ต้องไปพบแพทย์ตามนัดหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "28. วัคซีนที่ควรได้รับ", "text": "ควรได้รับวัคซีนอะไรบ้าง"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "30. โรคประจำตัว", "text": "หากมีโรคประจำตัวต้องดูแลอย่างไร"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "12px"
        }
    }

    group4 = {
        "type": "bubble", "size": "kilo",
        "header": {
            "type": "box", "layout": "vertical",
            "contents": [{"type": "text", "text": "🍲 การดูแลตัวเอง", "weight": "bold", "color": "#FFFFFF", "size": "md"}],
            "backgroundColor": "#F57C00", "paddingAll": "12px"
        },
        "body": {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "11. รับประทานอาหาร", "text": "ควรรับประทานอาหารอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "12. ออกกำลังกาย", "text": "สามารถออกกำลังกายได้หรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "17. ผู้ดูแลช่วยอะไรได้", "text": "ผู้ดูแลสามารถช่วยอะไรได้บ้าง"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "18. ผลสีเขียวปลอดภัยไหม", "text": "ผลประเมินสีเขียวหมายความว่าปลอดภัยแน่นอนหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "19. แชตบอตแทนแพทย์ได้ไหม", "text": "แชตบอตใช้แทนแพทย์ได้หรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "20. อ่อนเพลีย", "text": "ทำไมยังรู้สึกอ่อนเพลียหลังกลับบ้าน"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "21. ความจำ/สมาธิลดลง", "text": "ความจำหรือสมาธิลดลงเป็นเรื่องปกติหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "25. ดูแลช่องปาก", "text": "ทำไมต้องดูแลความสะอาดช่องปาก"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "26. พบญาติ/ออกนอกบ้าน", "text": "สามารถพบญาติหรือออกไปนอกบ้านได้หรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "27. สวมหน้ากาก", "text": "จำเป็นต้องสวมหน้ากากหรือไม่"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "29. เดินทางไกล", "text": "สามารถเดินทางไกลได้เมื่อใด"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "31. กินข้าวได้น้อย", "text": "หากรับประทานอาหารได้น้อยควรทำอย่างไร"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "33. กลับไปทำงาน", "text": "สามารถกลับไปทำงานหรือทำกิจกรรมตามปกติได้หรือไม่"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "12px"
        }
    }

    return {
        "type": "flex",
        "altText": "📚 คำถามที่ถามได้ทั้งหมด (33 ข้อ)",
        "contents": {
            "type": "carousel",
            "contents": [group1, group2, group3, group4]
        }
    }


def build_thanks_flex():
    """Flex Message สำหรับตอบคำขอบคุณ"""
    return {
        "type": "flex",
        "altText": "ยินดีให้คำปรึกษาค่ะ",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "SepCare AI", "weight": "bold", "color": "#FFFFFF", "size": "md"}],
                "backgroundColor": "#00897B", "paddingAll": "12px"
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ยินดีให้คำปรึกษาค่ะ 😊", "weight": "bold", "size": "md", "color": "#00897B", "wrap": True},
                    {"type": "text", "text": "หากมีข้อสงสัยหรือต้องการคำแนะนำด้านสุขภาพเพิ่มเติม สามารถพิมพ์สอบถามได้ตลอดเวลาเลยนะคะ 💙", "size": "sm", "color": "#444444", "wrap": True, "margin": "md"}
                ],
                "paddingAll": "15px"
            }
        }
    }


def build_faq_flex(question, answer):
    """Flex Message สำหรับ FAQ + auto-append 'ค่ะ'"""
    answer = (answer or '').strip()
    if answer and not answer.endswith(('ค่ะ', 'นะคะ', 'ครับ', 'คะ')):
        answer = answer.rstrip('.?! ') + ' ค่ะ'

    return {
        "type": "flex",
        "altText": "SepCare FAQ: " + (question[:50] if question else ""),
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "SepCare FAQ", "weight": "bold", "color": "#FFFFFF", "size": "md"},
                    {"type": "text", "text": "คำถามที่พบบ่อย", "color": "#E0F2F1", "size": "xs", "margin": "xs"}
                ],
                "backgroundColor": "#0277BD", "paddingAll": "12px"
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "❓ คำถาม", "weight": "bold", "size": "xs", "color": "#0277BD"},
                            {"type": "text", "text": question, "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"}
                        ]
                    },
                    {"type": "separator", "margin": "lg"},
                    {
                        "type": "box", "layout": "vertical", "margin": "lg",
                        "contents": [
                            {"type": "text", "text": "💡 คำตอบ", "weight": "bold", "size": "xs", "color": "#0277BD"},
                            {"type": "text", "text": answer, "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"}
                        ]
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

