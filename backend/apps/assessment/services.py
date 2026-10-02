def evaluate_daily_check(has_fever, has_wound, has_breathless, has_confused, has_less_eat):
    """
    Evaluates 5 symptom questions into green, yellow, or red level.
    """
    if not any([has_fever, has_wound, has_breathless, has_confused, has_less_eat]):
        return 'green'
    
    # Severe combination -> Red
    if has_confused and (has_fever or has_breathless or has_less_eat):
        return 'red'
    
    # Any single symptom -> Yellow
    return 'yellow'


def evaluate_sepsis_screening(data):
    """
    Evaluates Sepsis Screening data according to UK Sepsis Trust Community Care Decision Tree:
    Step 1: Risk Factors -> If NO, Sepsis Unlikely (Stop)
    Step 2: Infection Source -> If NO, Sepsis Unlikely (Stop)
    Step 3: Red Flags -> If YES, RED FLAG SEPSIS (Immediate Emergency Stop)
    Step 4: Amber Flags -> If YES, AMBER FLAG (Same-day Doctor Assessment), else ROUTINE CARE
    """
    # Step 3: Red Flags (7 items)
    red_keys = [
        'red_flag_mental', 'red_flag_rr_ge25', 'red_flag_o2_need',
        'red_flag_sbp_le90', 'red_flag_hr_gt130', 'red_flag_no_urine_18h',
        'red_flag_skin_change'
    ]
    has_red = any(bool(data.get(k, False)) for k in red_keys)

    if has_red:
        return True, False, "🚨 RED FLAG SEPSIS (วิกฤต): พบสัญญาณเตือนอันตรายระดับสีแดง! ให้เริ่มชุดการดูแลผู้ป่วยเซพซิสวิกฤต โปรดโทร 1669 หรือนำส่งห้องฉุกเฉินโรงพยาบาลทันทีโดยไม่รอ!"

    # Step 4: Amber Flags (10 items)
    amber_keys = [
        'amber_flag_behavior', 'amber_flag_activity_down', 'amber_flag_rr_21_24',
        'amber_flag_sbp_91_100', 'amber_flag_hr_91_120', 'amber_flag_spo2_lt92',
        'amber_flag_no_urine_12_18h', 'amber_flag_immuno', 'amber_flag_infection_sign',
        'amber_flag_temp_lt36'
    ]
    has_amber = any(bool(data.get(k, False)) for k in amber_keys)

    if has_amber:
        return False, True, "⚠️ AMBER FLAG (เฝ้าระวัง): พบสัญญาณเตือนระดับสีเหลือง ควรได้รับการประเมินภายในวันเดียวกันโดยแพทย์ทั่วไปหรือหัวหน้าทีมแพทย์ และพิจารณาความจำเป็นในการส่งต่อโรงพยาบาลโดยเร่งด่วน"

    # Step 1: Risk Factors
    risk_keys = ['age_over_75', 'immunocompromised', 'has_catheter', 'recent_surgery']
    has_risk = any(bool(data.get(k, False)) for k in risk_keys)

    if not has_risk:
        return False, False, "🟢 โอกาสเป็นภาวะเซพซิสน้อยมาก: ไม่พบปัจจัยเสี่ยง ควรพิจารณาการวินิจฉัยโรคอื่น และให้การดูแลสังเกตอาการตามปกติ"

    # Step 2: Infection Source
    inf_keys = [
        'infection_respiratory', 'infection_urinary', 'infection_skin',
        'infection_device', 'infection_brain', 'infection_surgery'
    ]
    has_infection = any(bool(data.get(k, False)) for k in inf_keys) or bool(data.get('infection_other', '').strip())

    if not has_infection:
        return False, False, "🟢 มีโอกาสน้อยที่จะเป็นภาวะเซพซิส: เนื่องจากไม่มีสัญญาณการติดเชื้อชัดเจน ควรพิจารณาการวินิจฉัยโรคอื่น และสังเกตอาการตามปกติ"

    return False, False, "🟢 ROUTINE CARE (ดูแลตามปกติ): ไม่พบสัญญาณเตือนสีเหลืองหรือสีแดง ให้การดูแลตามปกติ พร้อมคำแนะนำด้านความปลอดภัย หากอาการเปลี่ยนไปหรือแย่ลง ให้โทร 1669 ทันที"
