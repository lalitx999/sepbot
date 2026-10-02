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
            'spo2': request.data.get('spo2'),
        }

        serializer = VitalSignSerializer(data=data)
        if serializer.is_valid():
            vitals = serializer.save()

            # Push summary LINE message to user
            try:
                from linebot.handlers import push_line_message, notify_nurse_emergency

                v_details = []
                if vitals.temperature:
                    v_details.append(f"• อุณหภูมิ: {vitals.temperature} °C")
                if vitals.systolic_bp and vitals.diastolic_bp:
                    v_details.append(f"• ความดันโลหิต: {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg")
                elif vitals.systolic_bp:
                    v_details.append(f"• ความดันตัวบน (SBP): {vitals.systolic_bp} mmHg")
                if vitals.heart_rate:
                    v_details.append(f"• อัตราชีพจร: {vitals.heart_rate} ครั้ง/นาที")
                if vitals.respiratory_rate:
                    v_details.append(f"• อัตราการหายใจ: {vitals.respiratory_rate} ครั้ง/นาที")
                if vitals.spo2:
                    v_details.append(f"• ออกซิเจนในเลือด (SpO2): {vitals.spo2} %")

                detail_str = "\n".join(v_details) if v_details else "• บันทึกสำเร็จ"
                noti_msg = (
                    f"🩺 ขอบคุณที่บันทึกสุขภาพประจำวันค่ะ 💙\n\n"
                    f"📊 ค่าสัญญาณชีพที่คุณบันทึก:\n"
                    f"{detail_str}\n\n"
                    f"ระบบจะคอยติดตามและดูแลสุขภาพของคุณอย่างต่อเนื่องนะคะ 😊"
                )
                push_line_message(user.line_user_id, noti_msg)

                # Check if any vital sign is critically abnormal -> Alert Nurse Sai
                is_abnormal = False
                if vitals.spo2 and vitals.spo2 < 95:
                    is_abnormal = True
                if vitals.temperature and (vitals.temperature >= 38.0 or vitals.temperature <= 35.5):
                    is_abnormal = True
                if vitals.systolic_bp and (vitals.systolic_bp < 90 or vitals.systolic_bp > 140):
                    is_abnormal = True

                if is_abnormal:
                    notify_nurse_emergency(user.line_user_id, alert_type="emergency")

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
