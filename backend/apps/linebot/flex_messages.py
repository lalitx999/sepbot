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


def build_ask_nurse_flex():
    """
    Flex Message sent when user clicks "ถามพยาบาล" on Rich Menu or asks a
    question that doesn't match any FAQ. Hands the conversation off to a
    real nurse's personal LINE chat instead of the automated bot.
    """
    nurse_line_link = os.getenv('NURSE_LINE_PERSONAL_LINK', 'https://line.me/ti/p/~Siine8')
    nurse_phone = os.getenv('NURSE_CONTACT_PHONE', '0996244555')

    return {
        "type": "flex",
        "altText": "พูดคุยกับพยาบาลโครงการโดยตรง",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💬 ถามพยาบาล",
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
                        "text": "หากคำถามของคุณไม่ตรงกับ FAQ ที่มี สามารถกดปุ่มด้านล่างเพื่อพูดคุยกับพยาบาลโครงการโดยตรงได้เลยค่ะ",
                        "wrap": True,
                        "size": "sm",
                        "color": "#444444"
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
                            "label": f"📞 โทรพยาบาลโครงการ ({nurse_phone})",
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
    Strictly NO emojis. Clean medical teal banner theme.
    Displays only the AI answer in the card body.
    """
    nurse_line_link = os.getenv('NURSE_LINE_PERSONAL_LINK', 'https://line.me/ti/p/~Siine8')

    return {
        "type": "flex",
        "altText": "SepCare AI: คำแนะนำตามคู่มือการดูแลผู้ป่วยหลังภาวะเซพซิส",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "SepCare AI - คำแนะนำตามคู่มือ",
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
                            "label": "สอบถามพยาบาลเพิ่มเติม",
                            "uri": nurse_line_link
                        },
                        "style": "primary",
                        "color": "#005B5C"
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

