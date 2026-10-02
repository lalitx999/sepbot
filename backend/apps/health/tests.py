from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import FamilyGroup, LineUser
from .models import VitalSign

class HealthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fg = FamilyGroup.objects.create(code='FG22222')
        self.user = LineUser.objects.create(
            line_user_id='U_VITAL_USER',
            name='นายวัด สัญญาณชีพ',
            id_card='1234567890123',
            age=55,
            role='patient',
            family=self.fg,
            is_registered=True
        )

    def test_record_vital_signs(self):
        url = '/api/v1/health/vitals/'
        data = {
            'line_user_id': self.user.line_user_id,
            'temperature': 36.6,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'heart_rate': 72,
            'respiratory_rate': 16,
            'spo2': 99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        vitals = VitalSign.objects.get(user=self.user)
        self.assertEqual(vitals.temperature, 36.6)
        self.assertEqual(vitals.spo2, 99)
