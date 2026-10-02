from django.conf import settings
from faq.models import FAQ
from .flex_messages import build_greeting_flex, build_emergency_flex, build_ask_nurse_flex

import requests

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
    Utility function to reply a message back to LINE using replyToken.
    Supports FlexMessage dict or TextMessage dict with direct HTTP fallback.
    """
    access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not access_token or access_token == 'your_line_channel_access_token_here':
        print(f"[Mock Reply Message] Token: {reply_token} | Message: {message_dict}")
        return True

    # 1. Try SDK first
    try:
        from linebot.v3.messaging import (
            Configuration, ApiClient, MessagingApi,
            ReplyMessageRequest, FlexMessage, FlexContainer, TextMessage
        )
        configuration = Configuration(access_token=access_token)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            if isinstance(message_dict, dict) and message_dict.get('type') == 'flex':
                flex_content = FlexContainer.from_dict(message_dict['contents'])
                msg_obj = FlexMessage(
                    altText=message_dict.get('altText', 'Sepsis Care System'),
                    contents=flex_content
                )
            elif isinstance(message_dict, dict) and message_dict.get('type') == 'text':
                msg_obj = TextMessage(text=message_dict.get('text', ''))
            else:
                msg_obj = TextMessage(text=str(message_dict))

            request = ReplyMessageRequest(
                replyToken=reply_token,
                messages=[msg_obj]
            )
            line_bot_api.reply_message(request)
            return True
    except Exception as sdk_e:
        print(f"SDK Reply Warning, trying direct HTTP: {sdk_e}")

    # 2. Fallback to Direct HTTP API
    try:
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        if isinstance(message_dict, dict):
            msg_payload = message_dict
        else:
            msg_payload = {"type": "text", "text": str(message_dict)}

        body = {
            "replyToken": reply_token,
            "messages": [msg_payload]
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

        # Save Notification Log if user and family exist
        if user and user.family:
            NotificationLog.objects.create(
                user=user,
                family=user.family,
                type='emergency' if alert_type == 'emergency' else 'daily_check',
                message=alert_msg,
                is_sent=True,
                sent_at=timezone.now()
            )

        # Find all registered nurses or nurse contact in .env
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
    """
    text = text_content.strip()

    if text in ['ติดต่อฉุกเฉิน', 'ฉุกเฉิน', '1669', '🚨']:
        notify_nurse_emergency(line_user_id, alert_type="emergency")
        return build_emergency_flex()

    if text in ['ถามพยาบาล', 'พยาบาล', 'ติดต่อพยาบาล']:
        notify_nurse_emergency(line_user_id, alert_type="ask_nurse")
        return build_ask_nurse_flex()

    # 1. FAQ Search Engine match
    matched_faq = FAQ.objects.filter(question__icontains=text).first()
    if matched_faq:
        return {
            'type': 'text',
            'text': f"❓ **คำถาม**: {matched_faq.question}\n\n💡 **คำตอบ**: {matched_faq.answer}"
        }

    # 2. DeepSeek AI LLM Query (Anti-Hallucination)
    try:
        from .llm_service import query_deepseek_ai
        from .flex_messages import build_ai_response_flex
        from accounts.models import LineUser
        
        user = LineUser.objects.filter(line_user_id=line_user_id).first()
        u_ctx = f"ชื่อ: {user.name}, อายุ: {user.age}, โรคประจำตัว: {user.underlying_disease}" if user else None
        
        ai_response = query_deepseek_ai(text, user_context=u_ctx)
        if ai_response:
            return build_ai_response_flex(ai_response)
    except Exception as e:
        print(f"DeepSeek Query Error: {e}")

    # 3. Fallback to Nurse hand-off
    return build_ask_nurse_flex()
