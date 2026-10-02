from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FamilyGroup, LineUser
from .serializers import LineUserSerializer, RegisterSerializer

class RegisterView(APIView):
    """
    LIFF Registration Endpoint:
    Registers a new LineUser and pairs them into a FamilyGroup (Patient 1 + Caregiver 1).
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        line_user_id = data['line_user_id']
        family_code = data.get('family_code', '').strip().upper()

        # Check if user already registered
        user, created = LineUser.objects.get_or_create(
            line_user_id=line_user_id,
            defaults={
                'name': data['name'],
                'display_name': data.get('display_name', ''),
                'id_card': data['id_card'],
                'phone_number': data.get('phone_number', ''),
                'age': data['age'],
                'role': data['role'],
            }
        )

        if not created and user.is_registered:
            return Response({
                'message': 'ผู้ใช้นี้ทำการลงทะเบียนเรียบร้อยแล้ว',
                'user': LineUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        # Handle FamilyGroup association
        if data['role'] == 'caregiver':
            if not family_code:
                return Response({'error': 'ผู้ดูแลจำเป็นต้องกรอกรหัสครอบครัว (FGxxxxx) ของผู้ป่วย'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                family = FamilyGroup.objects.get(code=family_code)
            except FamilyGroup.DoesNotExist:
                return Response({'error': f'ไม่พบรหัสครอบครัว {family_code} กรุณาตรวจสอบรหัสจากผู้ป่วย'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if family_code:
                try:
                    family = FamilyGroup.objects.get(code=family_code)
                except FamilyGroup.DoesNotExist:
                    family = FamilyGroup.objects.create(code=FamilyGroup.generate_unique_code())
            else:
                family = FamilyGroup.objects.create(code=FamilyGroup.generate_unique_code())

        # Update user fields
        user.name = data['name']
        user.display_name = data.get('display_name', user.display_name)
        user.id_card = data['id_card']
        user.phone_number = data['phone_number']
        user.age = data['age']
        user.role = data['role']
        user.family = family
        user.is_registered = True
        user.registered_at = timezone.now()
        user.save()

        # Switch Rich Menu on LINE and push success notification
        try:
            from apps.linebot.rich_menu import switch_user_rich_menu
            from apps.linebot.handlers import push_line_message
            switch_user_rich_menu(user.line_user_id, is_registered=True)
            greeting_msg = (
                f"สวัสดีค่ะ 👋 ยินดีต้อนรับคุณ {user.name} สู่ SepCare\n"
                f"ผู้ช่วยดูแลสุขภาพสำหรับผู้สูงอายุหลังภาวะเซพซิสและครอบครัว 💙🩷\n\n"
                f"SepCare พร้อมช่วยคุณในการเดินทางการฟื้นตัวหลังจากผ่านภาวะเซพซิส\n\n"
                f"รหัสครอบครัวของคุณคือ: [{family.code}]\n\n"
                f"พิมพ์คำถามของคุณ หรือเลือกหัวข้อด้านล่างเพื่อเริ่มต้น\n"
                f"🚨 หากมีอาการฉุกเฉิน โปรดโทร 1669 ทันที ไม่ต้องรอการตอบกลับจากแชตบอต"
            )
            push_line_message(user.line_user_id, greeting_msg)
        except Exception as e:
            print(f"Rich Menu Switch Warning: {e}")

        patient_name = ""
        if family:
            patient = LineUser.objects.filter(family=family, role='patient').first()
            if patient:
                patient_name = patient.name

        user_data = LineUserSerializer(user).data
        user_data['patient_name'] = patient_name

        return Response({
            'message': 'ลงทะเบียนเรียบร้อยแล้ว',
            'user': user_data,
            'patient_name': patient_name
        }, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    """
    Fetch LineUser profile & FamilyGroup details
    """
    def get(self, request, line_user_id):
        try:
            user = LineUser.objects.get(line_user_id=line_user_id)
            return Response(LineUserSerializer(user).data)
        except LineUser.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)
