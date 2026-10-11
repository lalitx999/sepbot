"""
MEWS (Modified Early Warning Score) calculation service
Based on Thai Clinical Sepsis & Vital Signs Evaluation Matrix.
"""

def calculate_mews(temperature=None, systolic_bp=None, heart_rate=None,
                   respiratory_rate=None, consciousness=None, urine_output=None):
    """
    Calculates MEWS (0-15) and determines clinical risk level (green, yellow, red).
    Returns (total_score, risk_level, breakdown_dict)
    """
    scores = {}

    # 1. Temperature (°C)
    if temperature is not None:
        t = float(temperature)
        if t <= 35.0:
            scores['temperature'] = 2
        elif 35.1 <= t <= 36.0:
            scores['temperature'] = 1
        elif 36.1 <= t <= 38.0:
            scores['temperature'] = 0
        elif 38.1 <= t <= 38.4:
            scores['temperature'] = 1
        else: # >= 38.5
            scores['temperature'] = 2
    else:
        scores['temperature'] = 0

    # 2. Systolic BP (mmHg)
    if systolic_bp is not None:
        sbp = int(systolic_bp)
        if sbp <= 80:
            scores['systolic_bp'] = 3
        elif 81 <= sbp <= 90:
            scores['systolic_bp'] = 2
        elif 91 <= sbp <= 100:
            scores['systolic_bp'] = 1
        elif 101 <= sbp <= 180:
            scores['systolic_bp'] = 0
        elif 181 <= sbp <= 199:
            scores['systolic_bp'] = 1
        else: # >= 200
            scores['systolic_bp'] = 2
    else:
        scores['systolic_bp'] = 0

    # 3. Heart Rate (bpm)
    if heart_rate is not None:
        hr = int(heart_rate)
        if hr <= 40:
            scores['heart_rate'] = 3
        elif 41 <= hr <= 50:
            scores['heart_rate'] = 1
        elif 51 <= hr <= 100:
            scores['heart_rate'] = 0
        elif 101 <= hr <= 120:
            scores['heart_rate'] = 1
        elif 121 <= hr <= 139:
            scores['heart_rate'] = 2
        else: # >= 140
            scores['heart_rate'] = 3
    else:
        scores['heart_rate'] = 0

    # 4. Respiratory Rate (/min)
    if respiratory_rate is not None:
        rr = int(respiratory_rate)
        if rr <= 8:
            scores['respiratory_rate'] = 3
        elif 9 <= rr <= 20:
            scores['respiratory_rate'] = 0
        elif 21 <= rr <= 25:
            scores['respiratory_rate'] = 1
        elif 26 <= rr <= 35:
            scores['respiratory_rate'] = 2
        else: # > 35
            scores['respiratory_rate'] = 3
    else:
        scores['respiratory_rate'] = 0

    # 5. Consciousness
    if consciousness:
        c = str(consciousness).lower()
        if c == 'alert':
            scores['consciousness'] = 0
        elif c in ['confused', 'drowsy']:
            scores['consciousness'] = 1
        elif c == 'stupor':
            scores['consciousness'] = 2
        elif c == 'unconscious':
            scores['consciousness'] = 3
        else:
            scores['consciousness'] = 0
    else:
        scores['consciousness'] = 0

    # 6. Urine Output
    if urine_output:
        u = str(urine_output).lower()
        if u == 'ge_1000':
            scores['urine_output'] = 0
        elif u == '501_999':
            scores['urine_output'] = 1
        elif u == 'le_500':
            scores['urine_output'] = 2
        else:
            scores['urine_output'] = 0
    else:
        scores['urine_output'] = 0

    total_score = sum(scores.values())

    # Risk level determination:
    # Red: Total >= 4 OR any single parameter has score 3
    # Yellow: Total 2 - 3
    # Green: Total 0 - 1
    has_single_3 = any(s >= 3 for s in scores.values())
    if total_score >= 4 or has_single_3:
        risk_level = 'red'
    elif total_score >= 2:
        risk_level = 'yellow'
    else:
        risk_level = 'green'

    return total_score, risk_level, scores
