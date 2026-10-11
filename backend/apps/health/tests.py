from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import FamilyGroup, LineUser
from .models import VitalSign

class HealthAPITest(TestCase):
    def setUp(self):
        self.push = patch('linebot.handlers.push_line_message').start()
        self.emergency = patch('linebot.handlers.notify_nurse_emergency').start()
        self.addCleanup(patch.stopall)
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
            'consciousness': 'alert',
            'urine_output': 'ge_1000'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        vitals = VitalSign.objects.get(user=self.user)
        self.assertEqual(vitals.temperature, 36.6)
        self.assertEqual(vitals.consciousness, 'alert')
        self.push.assert_called_once()
        self.emergency.assert_not_called()

    def test_each_required_field_rejects_missing_null_and_blank(self):
        complete = dict(line_user_id=self.user.line_user_id, temperature=36.6,
                        systolic_bp=120, diastolic_bp=80, heart_rate=72,
                        respiratory_rate=16, consciousness='alert', urine_output='ge_1000')
        for field in complete.keys() - {'line_user_id'}:
            for missing in ('omitted', None, ''):
                with self.subTest(field=field, missing=missing):
                    payload = complete.copy()
                    if missing == 'omitted':
                        del payload[field]
                    else:
                        payload[field] = missing
                    response = self.client.post('/api/v1/health/vitals/', payload, format='json')
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.data)
        self.assertFalse(VitalSign.objects.exists())
        self.push.assert_not_called()

    def test_abnormal_vitals_only_send_confirmation(self):
        response = self.client.post('/api/v1/health/vitals/', dict(
            line_user_id=self.user.line_user_id, temperature=39,
            systolic_bp=85, diastolic_bp=60, heart_rate=100,
            respiratory_rate=25, consciousness='confused', urine_output='le_500'), format='json')
        self.assertEqual(response.status_code, 201)
        self.push.assert_called_once()
        self.emergency.assert_not_called()
