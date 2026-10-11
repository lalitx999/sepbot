from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import FamilyGroup, LineUser
from .models import DailyCheck, SepsisScreening

class AssessmentAPITest(TestCase):
    def setUp(self):
        self.push = patch('linebot.handlers.push_line_message').start()
        self.addCleanup(patch.stopall)
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

    def test_daily_check_yellow(self):
        response = self.client.post('/api/v1/assessment/daily-check/', {
            'line_user_id': self.user.line_user_id, 'has_fever': True}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['daily_check']['result_level'], 'yellow')
        self.push.assert_called_once()

    def test_screening_levels_and_line_summary_match(self):
        for flags, red, amber in [({}, False, False),
                                  ({'amber_flag_behavior': True}, False, True),
                                  ({'red_flag_mental': True}, True, False)]:
            with self.subTest(flags=flags):
                self.push.reset_mock()
                response = self.client.post('/api/v1/assessment/screening/', {
                    'line_user_id': self.user.line_user_id, **flags}, format='json')
                self.assertIn(response.status_code, (200, 201))
                screening = response.data['screening']
                self.assertEqual(screening['has_red_flag'], red)
                self.assertEqual(screening['has_amber_flag'], amber)
                self.assertIn(screening['result'], self.push.call_args.args[1])
