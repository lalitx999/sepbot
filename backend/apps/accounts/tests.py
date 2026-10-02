from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FamilyGroup, LineUser

class AccountsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_patient_creates_family_group(self):
        url = '/api/v1/accounts/register/'
        data = {
            'line_user_id': 'U_TEST_PATIENT_001',
            'name': 'นายทดสอบ ผู้ป่วย',
            'id_card': '1234567890123',
            'phone_number': '0812345678',
            'age': 65,
            'role': 'patient',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('family_code', response.data['user'])
        
        # Check DB
        user = LineUser.objects.get(line_user_id='U_TEST_PATIENT_001')
        self.assertEqual(user.role, 'patient')
        self.assertTrue(user.family.code.startswith('FG'))

    def test_register_caregiver_with_existing_family_code(self):
        # First register patient
        fg = FamilyGroup.objects.create(code='FG99999')
        patient = LineUser.objects.create(
            line_user_id='U_PATIENT_EXISTING',
            name='ผู้ป่วยสมาคม',
            id_card='1111111111111',
            phone_number='0812345678',
            age=70,
            role='patient',
            family=fg,
            is_registered=True
        )

        # Register caregiver with FG99999
        url = '/api/v1/accounts/register/'
        data = {
            'line_user_id': 'U_TEST_CAREGIVER_001',
            'name': 'นางทดสอบ ผู้ดูแล',
            'id_card': '9876543210987',
            'phone_number': '0898765432',
            'age': 40,
            'role': 'caregiver',
            'family_code': 'FG99999'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        caregiver = LineUser.objects.get(line_user_id='U_TEST_CAREGIVER_001')
        self.assertEqual(caregiver.family, fg)
        self.assertEqual(fg.members.count(), 2)

    def test_fetch_profile(self):
        fg = FamilyGroup.objects.create(code='FG12345')
        user = LineUser.objects.create(
            line_user_id='U_PROFILE_TEST',
            name='สมชาย โปรไฟล์',
            id_card='1234567890123',
            age=50,
            role='patient',
            family=fg,
            is_registered=True
        )
        url = f'/api/v1/accounts/profile/{user.line_user_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'สมชาย โปรไฟล์')
