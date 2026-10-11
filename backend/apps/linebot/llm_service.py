import os
import json
import re
import requests
from django.conf import settings

def clean_think_tags(text):
    """
    Strips internal reasoning / <think>...</think> tags emitted by reasoning models
    so the end patient receives only the concise final medical advice.
    """
    if not text:
        return ""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'</?think>', '', cleaned)
    return cleaned.strip()

def query_medical_ai(user_question, user_context=None):
    """
    Queries OpenAI, Groq, or DeepSeek API for medical and self-care advice.
    Strict medical safety boundaries:
      1. NEVER diagnose diseases (ห้ามวินิจฉัยโรคเด็ดขาด AI ไม่ใช่แพทย์)
      2. Advise on self-care, symptom monitoring, and proper care only (แนะนำการปฏิบัติตัวและการดูแลรักษาเบื้องต้นเท่านั้น)
      3. Strict topic lock: ONLY answer medical, health, and patient care questions. Politely decline off-topic queries.
      4. Emergency red flags: emphasize calling 1669 immediately when severe signs are detected.
    """
    openai_api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
    groq_api_key = getattr(settings, 'GROQ_API_KEY', None) or os.getenv('GROQ_API_KEY')
    deepseek_api_key = getattr(settings, 'DEEPSEEK_API_KEY', None) or os.getenv('DEEPSEEK_API_KEY')

    api_key = None
    url = None
    candidate_models = []
    provider = None

    if openai_api_key and openai_api_key not in ['your_openai_api_key_here', '']:
        api_key = openai_api_key.strip()
        url = "https://api.openai.com/v1/chat/completions"
        candidate_models = [
            os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'gpt-4o-mini',
            'gpt-4o',
        ]
        candidate_models = list(dict.fromkeys(candidate_models))
        provider = "OpenAI"
    elif groq_api_key and groq_api_key not in ['your_groq_api_key_here', '']:
        api_key = groq_api_key.strip()
        url = "https://api.groq.com/openai/v1/chat/completions"
        candidate_models = [
            os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant'),
            'llama-3.1-8b-instant',
            'openai/gpt-oss-20b',
        ]
        candidate_models = list(dict.fromkeys(candidate_models))
        provider = "Groq"
    elif deepseek_api_key and deepseek_api_key not in ['your_deepseek_api_key_here', '']:
        api_key = deepseek_api_key.strip()
        url = "https://api.deepseek.com/v1/chat/completions"
        candidate_models = [os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')]
        provider = "DeepSeek"
    else:
        print("[AI Service Warning] No valid OPENAI_API_KEY, GROQ_API_KEY, or DEEPSEEK_API_KEY configured.")
        return None

    system_prompt = (
        "คุณคือ 'SepCare AI' ผู้ช่วยอัจฉริยะด้านการแพทย์และการดูแลสุขภาพสำหรับผู้ป่วยและครอบครัว (เน้นการดูแลตนเองหลังภาวะเซพซิสและการดูแลสุขภาพทั่วไป)\n\n"
        "ข้อกำหนดและจริยธรรมทางการแพทย์ที่ต้องปฏิบัติตามอย่างเคร่งครัด:\n\n"
        "1. [ห้ามวินิจฉัยโรคเด็ดขาด (DO NOT DIAGNOSE)]:\n"
        "- คุณไม่ใช่แพทย์ และไม่สามารถทำหน้าที่วินิจฉัยโรคแทนแพทย์ได้ ห้ามฟันธงหรือบอกว่าผู้ป่วย 'เป็นโรค...' หรือ 'ติดเชื้อ... แน่นอน'\n"
        "- หากผู้ใช้ถามในเชิงให้วินิจฉัย เช่น 'หนูเป็นโรคอะไร', 'อาการแบบนี้คืออะไร': ให้ตอบว่าอาการดังกล่าวอาจเกิดได้จากหลายสาเหตุ และแนะนำให้ไปพบแพทย์เพื่อตรวจร่างกายอย่างละเอียดเสมอ\n\n"
        "2. [บทบาท: แนะนำการปฏิบัติตัวเบื้องต้นและการดูแลสุขภาพ (SELF-CARE & CARE ADVICE ONLY)]:\n"
        "- แนะนำการดูแลตนเอง, การดูแลแผล, การรับประทานอาหารและน้ำ, การพักผ่อน, การสังเกตอาการผิดปกติ, และการกินยาตามที่แพทย์สั่งอย่างเคร่งครัด\n"
        "- ห้ามสั่งยา หรือปรับขนาดยาเองเด็ดขาด ให้ย้ำเตือนให้ปรึกษาแพทย์หรือเภสัชกรประจำตัว\n"
        "- ใช้ภาษาไทยที่สุภาพ อบอุ่น ชัดเจน เข้าใจง่ายสำหรับผู้สูงอายุและญาติผู้ดูแล\n\n"
        "3. [จำกัดเฉพาะเรื่องการแพทย์และสุขภาพเท่านั้น (STRICT TOPIC LOCK)]:\n"
        "- ตอบเฉพาะคำถามที่เกี่ยวข้องกับ: การแพทย์, สุขภาพ, การพยาบาล, การดูแลผู้ป่วย, ยาและโภชนาการ, ภาวะเซพซิส, การดูแลตนเอง\n"
        "- หากผู้ใช้ถามเรื่องอื่นที่ไม่เกี่ยวข้องกับการแพทย์และสุขภาพ (เช่น การเมือง, หวย, กีฬา, ซ่อมรถ, บันเทิง, ไอที, คำถามทั่วไปที่ไม่เกี่ยวกับสุขภาพ): "
        "ให้ปฏิเสธอย่างสุภาพทันทีว่า: 'ขออภัยค่ะ SepCare AI ได้รับการออกแบบมาเพื่อดูแลและให้คำแนะนำด้านสุขภาพและการดูแลผู้ป่วยเท่านั้นค่ะ หากมีข้อสงสัยเกี่ยวกับอาการหรือการดูแลสุขภาพ สามารถสอบถามได้เลยนะคะ'\n\n"
        "4. [สัญญาณเตือนอันตรายฉุกเฉิน (EMERGENCY RED FLAGS)]:\n"
        "- หากผู้ป่วยมีหรือสงสัยอาการฉุกเฉินรุนแรง ได้แก่: พูดไม่ชัดหรือสับสนเฉียบพลัน, ซึมมาก ปลุกไม่ตื่น, หนาวสั่นรุนแรง, ปัสสาวะไม่ออกตลอดทั้งวัน, หายใจหอบเหนื่อยรุนแรง, ผิวหนังลายด่างเขียวคล้ำ: "
        "ต้องเน้นย้ำให้ผู้ป่วยหรือญาติรีบโทร 1669 ทันที หรือไปห้องฉุกเฉินโรงพยาบาลที่ใกล้ที่สุด โดยไม่ควรรอการตอบกลับในแชต\n\n"
        "5. [รูปแบบการตอบ]:\n"
        "- ตอบกระชับ ตรงประเด็น สุภาพ ไม่ใช้คำศัพท์แพทย์ที่ซับซ้อนเกินไป และสามารถแบ่งเป็นข้อย่อยอ่านง่ายได้"
    )

    context_info = f"\n\n[ข้อมูลผู้ป่วยในระบบ]: {user_context}" if user_context else ""

    messages = [
        {"role": "system", "content": system_prompt + context_info},
        {"role": "user", "content": user_question}
    ]

    try:
        temp_val = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))
    except ValueError:
        temp_val = 0.3

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for current_model in candidate_models:
        payload = {
            "model": current_model,
            "messages": messages,
            "temperature": temp_val,
            "max_tokens": 800
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                res_data = response.json()
                msg_obj = res_data['choices'][0]['message']
                raw_answer = (msg_obj.get('content') or '').strip()
                clean_answer = clean_think_tags(raw_answer)
                return clean_answer
            elif response.status_code in [400, 404] and ('model' in response.text or 'decommissioned' in response.text):
                print(f"[{provider} Model Warning] Model '{current_model}' unavailable, trying next candidate...")
                continue
            else:
                print(f"[{provider} API Error] Model: {current_model} | Status: {response.status_code} | Response: {response.text}")
                continue
        except Exception as e:
            print(f"[{provider} API Exception with {current_model}]: {e}")
            continue

    return None

# Backward compatibility alias
query_deepseek_ai = query_medical_ai
