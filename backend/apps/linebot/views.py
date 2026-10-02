import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .handlers import handle_incoming_text, reply_line_message, get_line_profile_name
from .flex_messages import build_greeting_flex
from .rich_menu import switch_user_rich_menu

@csrf_exempt
def line_webhook(request):
    """
    LINE Messaging API Webhook Endpoint
    Handles follow (greeting + locked rich menu) and message events.
    """
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed", status=405)

    signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
    body = request.body.decode('utf-8')

    try:
        data = json.loads(body)
        events = data.get('events', [])
        
        for event in events:
            event_type = event.get('type')
            source = event.get('source', {})
            line_user_id = source.get('userId')
            reply_token = event.get('replyToken')

            if event_type == 'follow':
                # User added bot / followed -> Fetch profile name, send personalized greeting flex & set locked rich menu
                display_name = get_line_profile_name(line_user_id) if line_user_id else ""
                print(f"New follower: {line_user_id} ({display_name})")
                greeting_flex = build_greeting_flex(display_name=display_name)
                if reply_token:
                    reply_line_message(reply_token, greeting_flex)
                
                # Switch user to locked rich menu (รอลงทะเบียน)
                if line_user_id:
                    switch_user_rich_menu(line_user_id, is_registered=False)

            elif event_type == 'message':
                message = event.get('message', {})
                if message.get('type') == 'text':
                    text = message.get('text')
                    response_msg = handle_incoming_text(line_user_id, text)
                    if reply_token and response_msg:
                        reply_line_message(reply_token, response_msg)
                    print(f"Handled message from {line_user_id}: {response_msg}")

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(f"Webhook processing error: {e}")
        return JsonResponse({'status': 'ok'}) # Return 200 OK to LINE API to prevent retries
