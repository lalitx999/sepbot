from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from accounts.models import LineUser
from .models import VitalSign
from .serializers import VitalSignSerializer

class VitalSignView(APIView):
    """
    Submit / Retrieve Vital Signs
    """
    def post(self, request):
        line_user_id = request.data.get('line_user_id')
        try:
            user = LineUser.objects.get(line_user_id=line_user_id)
        except LineUser.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)

        if not user.family:
            return Response({'error': 'ผู้ใช้ยังไม่ได้ผูกกับกลุ่มครอบครัว'}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()
        data = {
            'user': user.id,
            'family': user.family.id,
            'date': today,
            'temperature': request.data.get('temperature'),
            'heart_rate': request.data.get('heart_rate'),
            'systolic_bp': request.data.get('systolic_bp'),
            'diastolic_bp': request.data.get('diastolic_bp'),
            'respiratory_rate': request.data.get('respiratory_rate'),
            'consciousness': request.data.get('consciousness'),
            'urine_output': request.data.get('urine_output'),
        }

        serializer = VitalSignSerializer(data=data)
        if serializer.is_valid():
            vitals = serializer.save()

            # Calculate MEWS (Modified Early Warning Score)
            try:
                from .services import calculate_mews
                mews_score, mews_level, mews_breakdown = calculate_mews(
                    temperature=vitals.temperature,
                    systolic_bp=vitals.systolic_bp,
                    heart_rate=vitals.heart_rate,
                    respiratory_rate=vitals.respiratory_rate,
                    consciousness=vitals.consciousness,
                    urine_output=vitals.urine_output,
                )
                vitals.mews_score = mews_score
                vitals.mews_level = mews_level
                vitals.save(update_fields=['mews_score', 'mews_level'])
            except Exception as e:
                print(f"MEWS Calculation Error: {e}")

            # Push summary LINE message to user (Encouragement only, NO nurse emergency alarm)
            try:
                from linebot.handlers import push_line_message

                v_details = []
                if vitals.temperature:
                    v_details.append(f"• อุณหภูมิ: {vitals.temperature} °C")
                if vitals.systolic_bp and vitals.diastolic_bp:
                    v_details.append(f"• ความดันโลหิต: {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg")
                elif vitals.systolic_bp:
                    v_details.append(f"• ความดันตัวบน (SBP): {vitals.systolic_bp} mmHg")
                if vitals.heart_rate:
                    v_details.append(f"• อัตราการเต้นของหัวใจ: {vitals.heart_rate} ครั้ง/นาที")
                if vitals.respiratory_rate:
                    v_details.append(f"• อัตราการหายใจ: {vitals.respiratory_rate} ครั้ง/นาที")
                if vitals.consciousness:
                    v_details.append(f"• ความรู้สึกตัว: {vitals.get_consciousness_display()}")
                if vitals.urine_output:
                    v_details.append(f"• ปริมาณปัสสาวะต่อวัน: {vitals.get_urine_output_display()}")

                detail_str = "\n".join(v_details) if v_details else "• บันทึกสำเร็จ"
                noti_msg = (
                    f"🩺 ขอบคุณที่บันทึกสุขภาพประจำวันค่ะ 💙\n\n"
                    f"📊 ค่าสัญญาณชีพที่คุณบันทึก:\n"
                    f"{detail_str}\n\n"
                    f"SepCare จะคอยติดตามและดูแลสุขภาพของคุณอย่างต่อเนื่องนะคะ 😊"
                )
                push_line_message(user.line_user_id, noti_msg)

            except Exception as e:
                print(f"Vital Signs LINE Push Warning: {e}")

            return Response({
                'message': 'บันทึกสัญญาณชีพเรียบร้อยแล้ว',
                'vitals': VitalSignSerializer(vitals).data
            }, status=status.HTTP_201_CREATED)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, line_user_id):
        try:
            user = LineUser.objects.get(line_user_id=line_user_id)
            vitals = VitalSign.objects.filter(user=user).order_by('-date', '-recorded_at')
            return Response(VitalSignSerializer(vitals, many=True).data)
        except LineUser.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)
