from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from accounts.models import LineUser
from .models import DailyCheck, SepsisScreening
from .serializers import DailyCheckSerializer, SepsisScreeningSerializer
from .services import evaluate_daily_check, evaluate_sepsis_screening

class DailyCheckView(APIView):
    """
    Submit / Fetch Daily Symptom Check
    """
    def post(self, request):
        line_user_id = request.data.get('line_user_id')
        try:
            user = LineUser.objects.get(line_user_id=line_user_id)
        except LineUser.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)

        if not user.family:
            return Response({'error': 'ผู้ใช้ยังไม่ได้ผูกกับกลุ่มครอบครัว'}, status=status.HTTP_400_BAD_REQUEST)

        has_fever = bool(request.data.get('has_fever', False))
        has_wound = bool(request.data.get('has_wound', False))
        has_breathless = bool(request.data.get('has_breathless', False))
        has_confused = bool(request.data.get('has_confused', False))
        has_less_eat = bool(request.data.get('has_less_eat', False))

        result_level = evaluate_daily_check(has_fever, has_wound, has_breathless, has_confused, has_less_eat)

        today = timezone.now().date()
        daily_check, created = DailyCheck.objects.update_or_create(
            user=user,
            date=today,
            defaults={
                'family': user.family,
                'has_fever': has_fever,
                'fever_detail': request.data.get('fever_detail', ''),
                'has_wound': has_wound,
                'wound_detail': request.data.get('wound_detail', ''),
                'has_breathless': has_breathless,
                'breathless_detail': request.data.get('breathless_detail', ''),
                'has_confused': has_confused,
                'confused_detail': request.data.get('confused_detail', ''),
                'has_less_eat': has_less_eat,
                'less_eat_detail': request.data.get('less_eat_detail', ''),
                'result_level': result_level,
                'responder': request.data.get('responder', 'patient'),
                'responded_at': timezone.now(),
            }
        )

        try:
            from linebot.handlers import push_line_message
            push_line_message(
                user.line_user_id,
                "ขอบคุณที่ประเมินอาการในวันนี้ อย่าลืมเช็กอาการทุกวันนะคะ 💙"
            )
        except Exception as e:
            print(f"Daily check encouragement push warning: {e}")

        return Response({
            'message': 'บันทึกการประเมินเรียบร้อยแล้ว',
            'daily_check': DailyCheckSerializer(daily_check).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SepsisScreeningView(APIView):
    """
    Submit / Fetch Sepsis Screening
    """
    def post(self, request):
        line_user_id = request.data.get('line_user_id')
        try:
            user = LineUser.objects.get(line_user_id=line_user_id)
        except LineUser.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)

        if not user.family:
            return Response({'error': 'ผู้ใช้ยังไม่ได้ผูกกับกลุ่มครอบครัว'}, status=status.HTTP_400_BAD_REQUEST)

        has_red, has_amber, summary = evaluate_sepsis_screening(request.data)

        today = timezone.now().date()
        screening_data = {
            'family': user.family,
            'age_over_75': bool(request.data.get('age_over_75', False)),
            'immunocompromised': bool(request.data.get('immunocompromised', False)),
            'has_catheter': bool(request.data.get('has_catheter', False)),
            'recent_surgery': bool(request.data.get('recent_surgery', False)),
            'infection_respiratory': bool(request.data.get('infection_respiratory', False)),
            'infection_urinary': bool(request.data.get('infection_urinary', False)),
            'infection_skin': bool(request.data.get('infection_skin', False)),
            'infection_device': bool(request.data.get('infection_device', False)),
            'infection_brain': bool(request.data.get('infection_brain', False)),
            'infection_surgery': bool(request.data.get('infection_surgery', False)),
            'infection_other': request.data.get('infection_other', ''),
            'red_flag_mental': bool(request.data.get('red_flag_mental', False)),
            'red_flag_rr_ge25': bool(request.data.get('red_flag_rr_ge25', False)),
            'red_flag_o2_need': bool(request.data.get('red_flag_o2_need', False)),
            'red_flag_sbp_le90': bool(request.data.get('red_flag_sbp_le90', False)),
            'red_flag_hr_gt130': bool(request.data.get('red_flag_hr_gt130', False)),
            'red_flag_no_urine_18h': bool(request.data.get('red_flag_no_urine_18h', False)),
            'red_flag_skin_change': bool(request.data.get('red_flag_skin_change', False)),
            'amber_flag_behavior': bool(request.data.get('amber_flag_behavior', False)),
            'amber_flag_activity_down': bool(request.data.get('amber_flag_activity_down', False)),
            'amber_flag_rr_21_24': bool(request.data.get('amber_flag_rr_21_24', False)),
            'amber_flag_sbp_91_100': bool(request.data.get('amber_flag_sbp_91_100', False)),
            'amber_flag_hr_91_120': bool(request.data.get('amber_flag_hr_91_120', False)),
            'amber_flag_spo2_lt92': bool(request.data.get('amber_flag_spo2_lt92', False)),
            'amber_flag_no_urine_12_18h': bool(request.data.get('amber_flag_no_urine_12_18h', False)),
            'amber_flag_immuno': bool(request.data.get('amber_flag_immuno', False)),
            'amber_flag_infection_sign': bool(request.data.get('amber_flag_infection_sign', False)),
            'amber_flag_temp_lt36': bool(request.data.get('amber_flag_temp_lt36', False)),
            'has_red_flag': has_red,
            'has_amber_flag': has_amber,
            'result': summary,
        }

        screening, created = SepsisScreening.objects.update_or_create(
            user=user,
            date=today,
            defaults=screening_data
        )

        try:
            from linebot.handlers import push_line_message
            push_line_message(
                user.line_user_id,
                f"📋 **ผลการคัดกรองภาวะเซพซิสในชุมชน**:\n\n{summary}"
            )
        except Exception as e:
            print(f"Sepsis screening push warning: {e}")

        return Response({
            'message': 'บันทึกการคัดกรองเซพซิสเรียบร้อยแล้ว',
            'screening': SepsisScreeningSerializer(screening).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
