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
    """
    emergency_phone = os.getenv('EMERGENCY_PHONE_1669', '1669')
    police_phone = os.getenv('EMERGENCY_PHONE_191', '191')
    hospital_phone = os.getenv('HOSPITAL_CHULA_PHONE', '022564000')
    nurse_phone = os.getenv('NURSE_CONTACT_PHONE', '0996244555')

    return {
        "type": "flex",
        "altText": "🚨 รายชื่อเบอร์โทรฉุกเฉินและสัญญาณอันตราย (Red Flags)",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🚨 ติดต่อฉุกเฉิน / อาการวิกฤต",
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
                        "text": "หากมีอาการดังต่อไปนี้ โทร 1669 ทันที:",
                        "weight": "bold",
                        "color": "#D32F2F",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "• พูดไม่ชัดหรือมีอาการสับสน\n• หนาวสั่นอย่างรุนแรงหรือปวดกล้ามเนื้อ\n• ไม่มีปัสสาวะออกเลยตลอดทั้งวัน\n• หายใจลำบากอย่างรุนแรง\n• ผิวหนังมีลายด่างสีเทาซีด เขียวคล้ำ หรือซีดมาก",
                        "wrap": True,
                        "size": "xs",
                        "color": "#333333",
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
                            "label": "📞 โทร 1669 (การแพทย์ฉุกเฉิน)",
                            "uri": f"tel:{emergency_phone}"
                        },
                        "style": "primary",
                        "color": "#D32F2F"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "📞 โทร 191 (เหตุด่วนเหตุร้าย)",
                            "uri": f"tel:{police_phone}"
                        },
                        "style": "secondary"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": f"📞 โรงพยาบาลจุฬาลงกรณ์ ({hospital_phone})",
                            "uri": f"tel:{hospital_phone}"
                        },
                        "style": "secondary"
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

