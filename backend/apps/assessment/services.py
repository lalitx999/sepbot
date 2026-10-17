def evaluate_daily_check(has_fever=False, has_confused=False, has_breathless=False, has_sputum=False, has_urine=False, has_less_eat=False, **kwargs):
    """
    Evaluates 6 daily check questions according to the new scoring rule:
    0-1 symptoms: Green (อาการปกติ ติดตามอาการทุกวัน)
    2-3 symptoms: Yellow (เฝ้าระวัง กรุณาติดต่อพยาบาลวิจัยและเฝ้าระวังอาการทุก 12 ชั่วโมง)
    >3 symptoms: Red (อาการวิกฤต กรุณาผู้ป่วยส่งโรงพยาบาลด่วนหรือโทร 1669 ทันที)
    """
    symptoms = [has_fever, has_confused, has_breathless, has_sputum, has_urine, has_less_eat]
    score = sum(1 for s in symptoms if bool(s))

    if score <= 1:
        return 'green', 'อาการปกติ ติดตามอาการทุกวัน'
    elif 2 <= score <= 3:
        return 'yellow', 'เฝ้าระวัง กรุณาติดต่อพยาบาลวิจัยและเฝ้าระวังอาการทุก 12 ชั่วโมง'
    else:
        return 'red', 'อาการวิกฤต กรุณาผู้ป่วยส่งโรงพยาบาลด่วนหรือโทร 1669 ทันที'


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
        return True, False, "🚨 สัญญาณเตือนระดับสีแดง (Red Flags): พบสัญญาณเตือนอันตรายระดับสีแดง! ให้เริ่มชุดการดูแลผู้ป่วยภาวะเซพซิสที่มีสัญญาณเตือนระดับสีแดง: โทร 1669 และประสานการส่งผู้ป่วยไปโรงพยาบาลโดยรถพยาบาลที่มีไฟและเสียงสัญญาณฉุกเฉิน แจ้งทีมรถพยาบาลให้แจ้งเตือนโรงพยาบาลล่วงหน้าว่าเป็นผู้ป่วยที่มีภาวะเซพซิสที่มีสัญญาณเตือนระดับสีแดง"

    # Step 4: Amber Flags (10 items)
    amber_keys = [
        'amber_flag_behavior', 'amber_flag_activity_down', 'amber_flag_rr_21_24',
        'amber_flag_sbp_91_100', 'amber_flag_hr_91_120', 'amber_flag_spo2_lt92',
        'amber_flag_no_urine_12_18h', 'amber_flag_immuno', 'amber_flag_infection_sign',
        'amber_flag_temp_lt36'
    ]
    has_amber = any(bool(data.get(k, False)) for k in amber_keys)

    if has_amber:
        return False, True, (
            "⚠️ สัญญาณเตือนระดับสีเหลือง (Amber Flags): พบสัญญาณเตือนระดับสีเหลือง!\n\n"
            "1. รับการประเมินภายในวันเดียวกันโดยแพทย์ทั่วไปหรือหัวหน้าทีมแพทย์\n"
            "2. จำเป็นต้องส่งต่อผู้ป่วยไปยังโรงพยาบาลโดยเร่งด่วนหรือไม่\n"
            "3. เห็นชอบและบันทึกแผนการดูแลรักษาต่อเนื่อง (รวมถึงความถี่ในการติดตามสังเกตอาการและแผนการประเมินซ้ำครั้งที่สอง)"
        )

    # Step 1: Risk Factors
    risk_keys = ['age_over_75', 'immunocompromised', 'has_catheter', 'recent_surgery']
    has_risk = any(bool(data.get(k, False)) for k in risk_keys)

    if not has_risk:
        return False, False, "🟢 ไม่พบปัจจัยเสี่ยงต่อภาวะเซพซิส: โอกาสเป็นภาวะเซพซิสน้อยมาก ควรพิจารณาการวินิจฉัยโรคอื่น และให้การดูแลตามปกติ"

    # Step 2: Infection Source
    inf_keys = [
        'infection_respiratory', 'infection_urinary', 'infection_skin',
        'infection_device', 'infection_brain', 'infection_surgery'
    ]
    has_infection = any(bool(data.get(k, False)) for k in inf_keys) or bool(data.get('infection_other', '').strip())

    if not has_infection:
        return False, False, "🟢 ไม่มีสาเหตุของการติดเชื้อ: มีโอกาสน้อยที่จะเป็นภาวะเซพซิส ควรพิจารณาการวินิจฉัยโรคอื่น"

    return False, False, "🟢 ให้การดูแลตามปกติ (Routine Care): ไม่พบสัญญาณเตือนระดับสีเหลือง พร้อมให้คำแนะนำด้านความปลอดภัย โดยแนะนำให้โทร 1669 ทันที หากมีอาการ: พูดไม่ชัดหรือมีอาการสับสน, ซึมลง หมดสติ หรือไม่รู้สึกตัว, หนาวสั่นอย่างรุนแรงหรือมีอาการปวดกล้ามเนื้อ, ไม่มีปัสสาวะออกเลย (ตลอดทั้งวัน), หายใจลำบากอย่างรุนแรง, 'รู้สึกเหมือนกำลังจะตาย', หรือผิวหนังมีลายด่าง สีเทาซีด/เขียวคล้ำ"
