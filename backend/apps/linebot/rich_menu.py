import os
from django.conf import settings

def switch_user_rich_menu(line_user_id, is_registered=True):
    """
    Switches user's rich menu between locked (รอลงทะเบียน) and unlocked (เมนูใช้งาน 6 ปุ่ม).
    Calls LINE Messaging API when LINE credentials are provided.
    """
    access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not access_token or access_token == 'your_line_channel_access_token_here':
        print(f"[Mock Rich Menu Switch] LineUser: {line_user_id} -> Registered: {is_registered}")
        return True

    try:
        from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
        configuration = Configuration(access_token=access_token)
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            if is_registered:
                rich_menu_id = os.getenv('LINE_RICH_MENU_REGISTERED_ID', '')
                if rich_menu_id:
                    line_bot_api.link_rich_menu_id_to_user(line_user_id, rich_menu_id)
                    print(f"Linked Registered Rich Menu {rich_menu_id} to user {line_user_id}")
            else:
                rich_menu_id = os.getenv('LINE_RICH_MENU_LOCKED_ID', '')
                if rich_menu_id:
                    line_bot_api.link_rich_menu_id_to_user(line_user_id, rich_menu_id)
                    print(f"Linked Locked Rich Menu {rich_menu_id} to user {line_user_id}")
            return True
    except Exception as e:
        print(f"Failed to switch Rich Menu: {e}")
        return False
