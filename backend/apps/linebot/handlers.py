import re
import threading
import requests
from django.conf import settings
from faq.models import FAQ
from .flex_messages import (
    build_greeting_flex,
    build_greeting_chat_flex,
    build_all_questions_flex,
    build_thanks_flex,
    build_faq_flex,
    build_emergency_flex,
    build_default_help_flex,
    build_ebook_flex,
    build_ai_response_flex,
)

GREETING_REGEX = re.compile(
    r'^(สวัสดี|หวัดดี|ดีครับ|ดีค่ะ|ดีจ้า|ว่าไง|hello|hi|hey|good\s*(morning|afternoon|evening))'
    r'(\s*(ครับ|ค่ะ|คับ|จ้า|นะ|คะ|นะคะ|นะครับ))?\s*[!?.]*\s*$',
    re.IGNORECASE
)

THANKS_REGEX = re.compile(
    r'^(ขอบคุณ|ขอบใจ|thanks|thank\s*you|thx)'
    r'(\s*(มาก|มากๆ|หลายๆ))?'
    r'(\s*(ครับ|ค่ะ|คับ|จ้า|นะ|คะ|นะคะ|นะครับ))?\s*[!?.]*\s*$',
    re.IGNORECASE
)


def push_line_message(line_user_id, text_message):
    """
    Utility function to push text message to a specific LINE user ID.
    Supports linebot SDK and direct HTTP requests fallback.
    """
    access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not access_token or access_token == 'your_line_channel_access_token_here':
        print(f"[Mock Push Message] To: {line_user_id} | Message: {text_message}")
        return True

    try:
        from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
        configuration = Configuration(access_token=access_token)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            request = PushMessageRequest(
                to=line_user_id,
                messages=[TextMessage(text=text_message)]
            )
            line_bot_api.push_message(request)
            return True
    except Exception as e:
        print(f"SDK Push Warning, trying direct HTTP: {e}")
        try:
            url = "https://api.line.me/v2/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            body = {
                "to": line_user_id,
                "messages": [{"type": "text", "text": text_message}]
            }
            res = requests.post(url, headers=headers, json=body, timeout=5)
            return res.status_code == 200
        except Exception as http_e:
            print(f"HTTP Push Error: {http_e}")
            return False


def get_line_profile_name(line_user_id):
    """
    Fetches user's display name from LINE Profile API.
    """
    access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not access_token or access_token == 'your_line_channel_access_token_here':
        return ""

    try:
        from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
        configuration = Configuration(access_token=access_token)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            profile = line_bot_api.get_profile(line_user_id)
            return profile.display_name
    except Exception as e:
        print(f"Error fetching LINE profile: {e}")
        return ""


def reply_line_message(reply_token, message_dict):
    """
    Utility function to reply with Flex Message or Text using LINE Messaging API.
    Supports single message dict or a list of messages.
    """
    access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not access_token or access_token == 'your_line_channel_access_token_here':
        print(f"[Mock Reply Message] Token: {reply_token}")
        return True

    msg_list = message_dict if isinstance(message_dict, list) else [message_dict]

    try:
        from linebot.v3.messaging import (
            Configuration, ApiClient, MessagingApi,
            ReplyMessageRequest, FlexMessage, FlexContainer, TextMessage
        )
        configuration = Configuration(access_token=access_token)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            msg_objs = []
            for item in msg_list:
                if isinstance(item, dict) and item.get('type') == 'flex':
                    flex_content = FlexContainer.from_dict(item['contents'])
                    msg_objs.append(FlexMessage(
                        altText=item.get('altText', 'SepCare System'),
                        contents=flex_content
                    ))
                elif isinstance(item, dict) and item.get('type') == 'text':
                    msg_objs.append(TextMessage(text=item.get('text', '')))
                else:
                    msg_objs.append(TextMessage(text=str(item)))

            request = ReplyMessageRequest(
                replyToken=reply_token,
                messages=msg_objs
            )
            line_bot_api.reply_message(request)
            print(f"[LINE Reply OK via SDK] {len(msg_objs)} msgs")
            return True
    except Exception as sdk_e:
        print(f"SDK Reply Warning, trying direct HTTP: {sdk_e}")

    try:
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        msg_payloads = []
        for item in msg_list:
            if isinstance(item, dict):
                msg_payloads.append(item)
            else:
                msg_payloads.append({"type": "text", "text": str(item)})

        body = {
            "replyToken": reply_token,
            "messages": msg_payloads
        }
        res = requests.post(url, headers=headers, json=body, timeout=5)
        return res.status_code == 200
    except Exception as http_e:
        print(f"HTTP Reply Error: {http_e}")
        return False


def notify_nurse_emergency(line_user_id, alert_type="ask_nurse"):
    """
    Looks up requesting patient/caregiver details and pushes real-time alert card to Nurse Sai (Nurses).
    """
    try:
        from accounts.models import LineUser
        from notification.models import NotificationLog
        from django.utils import timezone
        
        user = LineUser.objects.filter(line_user_id=line_user_id).first()
        user_name = user.name if user else "ผู้ป่วยไม่ระบุชื่อ"
        family_code = user.family.code if (user and user.family) else "ไม่ระบุ"
        user_role = "ผู้ป่วย" if (user and user.role == 'patient') else ("ผู้ดูแล" if (user and user.role == 'caregiver') else "พยาบาล")
        disease_info = user.underlying_disease if (user and user.underlying_disease) else "ไม่มี/ไม่ระบุ"
        phone_info = user.phone_number if (user and user.phone_number) else "ไม่ระบุ"

        alert_title = "🚨 แจ้งเตือนฉุกเฉิน!" if alert_type == "emergency" else "💬 ขอความช่วยเหลือ / ถามพยาบาล"
        alert_msg = (
            f"{alert_title}\n\n"
            f"👤 ผู้ขอความช่วยเหลือ: คุณ{user_name} ({user_role})\n"
            f"📞 เบอร์โทรศัพท์: {phone_info}\n"
            f"🏠 รหัสครอบครัว: [{family_code}]\n"
            f"🩺 โรคประจำตัว: {disease_info}\n"
            f"🆔 LINE User ID: {line_user_id}\n\n"
            f"กรุณาติดต่อกลับผู้ป่วยโดยเร็วที่สุดค่ะ 💙"
        )

        if user and user.family:
            NotificationLog.objects.create(
                user=user,
                family=user.family,
                type='emergency' if alert_type == 'emergency' else 'daily_check',
                message=alert_msg,
                is_sent=True,
                sent_at=timezone.now()
            )

        nurse_uids = set(LineUser.objects.filter(role='nurse').values_list('line_user_id', flat=True))
        env_nurse_uid = getattr(settings, 'NURSE_LINE_USER_ID', '').strip()
        if env_nurse_uid:
            nurse_uids.add(env_nurse_uid)

        for uid in nurse_uids:
            if uid:
                push_line_message(uid, alert_msg)
            
    except Exception as e:
        print(f"Error notifying nurse: {e}")


def handle_incoming_text(line_user_id, text_content):
    """
    Processes incoming text messages from LINE webhook.
    Features:
      - Interactive greeting and thanks recognition
      - Magic keyword '__SHOW_ALL_QUESTIONS__' for 33 FAQ carousel
      - Emergency contact (single infographic card + 1669)
      - Direct nurse hand-off
      - E-book quick access
      - FAQ database matching
      - OpenAI Medical AI (self-care & healthcare advisor, strict diagnosis guardrails, topic lock)
    """
    text = (text_content or '').strip()

    # 1. Magic keyword: ดูคำถามทั้งหมด 33 ข้อ (Carousel)
    if text == '__SHOW_ALL_QUESTIONS__':
        return build_all_questions_flex()

    # 2. Greetings Recognition (สวัสดี, สวัสดีค่ะ, สวัสดีครับ, ดีจ้า, etc.)
    if GREETING_REGEX.match(text):
        try:
            from accounts.models import LineUser
            user = LineUser.objects.filter(line_user_id=line_user_id).first()
            display_name = user.name if (user and user.name) else ""
        except Exception:
            display_name = ""
        return build_greeting_chat_flex(display_name=display_name)

    # 3. Thanks Recognition (ขอบคุณ, ขอบคุณค่ะ, ขอบคุณครับ, thanks)
    if THANKS_REGEX.match(text):
        return build_thanks_flex()

    # 4. Emergency (Single Infographic card + call 1669, async nurse alert)
    if text in ['ติดต่อฉุกเฉิน', 'ฉุกเฉิน', '1669', '🚨']:
        threading.Thread(target=notify_nurse_emergency, args=(line_user_id, "emergency"), daemon=True).start()
        return [build_emergency_flex()]

    # 5. E-Book quick link
    if text.lower() in ['ebook', 'e-book', 'อีบุ๊ค', 'คู่มือ', 'สมุดคู่มือ', 'เปิดหนังสือ', 'อ่านหนังสือ', 'หนังสือ']:
        return build_ebook_flex()

    # 6. FAQ exact / high similarity match
    try:
        matched_faq = FAQ.objects.filter(question__iexact=text).first()
        if not matched_faq and len(text) >= 8:
            candidate = FAQ.objects.filter(question__icontains=text).first()
            if candidate and len(text) >= len(candidate.question) * 0.6:
                matched_faq = candidate
        if matched_faq:
            return build_faq_flex(matched_faq.question, matched_faq.answer)
    except Exception as db_e:
        print(f"FAQ lookup exception: {db_e}")

    # 7. Medical AI LLM Query (Self-care & healthcare advisor with medical guardrails)
    try:
        from .llm_service import query_medical_ai
        from accounts.models import LineUser
        
        user = LineUser.objects.filter(line_user_id=line_user_id).first()
        u_ctx = f"ชื่อ: {user.name}, อายุ: {user.age}, โรคประจำตัว: {user.underlying_disease}" if user else None
        
        ai_response = query_medical_ai(text, user_context=u_ctx)
        if ai_response:
            return build_ai_response_flex(ai_response)
    except Exception as e:
        print(f"Medical AI Query Error: {e}")

    # 8. Fallback to Default Help guidance
    return build_default_help_flex()
