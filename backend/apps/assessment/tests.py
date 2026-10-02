from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import FamilyGroup, LineUser
from .models import DailyCheck, SepsisScreening

class AssessmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fg = FamilyGroup.objects.create(code='FG11111')
        self.user = LineUser.objects.create(
            line_user_id='U_ASSESSMENT_USER',
            name='นายประเมิน อาการ',
            id_card='1234567890123',
            age=60,
            role='patient',
            family=self.fg,
            is_registered=True
        )

    def test_daily_check_green(self):
        url = '/api/v1/assessment/daily-check/'
        data = {
            'line_user_id': self.user.line_user_id,
            'has_fever': False,
            'has_wound': False,
            'has_breathless': False,
            'has_confused': False,
            'has_less_eat': False,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['daily_check']['result_level'], 'green')

    def test_daily_check_red(self):
        url = '/api/v1/assessment/daily-check/'
        data = {
            'line_user_id': self.user.line_user_id,
            'has_fever': True,
            'has_confused': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['daily_check']['result_level'], 'red')

    def test_sepsis_screening_red_flag(self):
        url = '/api/v1/assessment/screening/'
        data = {
            'line_user_id': self.user.line_user_id,
            'red_flag_mental': True,
            'red_flag_rr_ge25': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['screening']['has_red_flag'])
