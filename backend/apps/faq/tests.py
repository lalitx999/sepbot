from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FAQ

class FAQAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        FAQ.objects.create(
            order=1,
            category='general',
            question='ภาวะเซพซิสคืออะไร?',
            answer='คือภาวะติดเชื้อในกระแสเลือดขั้นรุนแรง'
        )

    def test_list_faq(self):
        url = '/api/v1/faq/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_faq_matching(self):
        url = '/api/v1/faq/search/'
        data = {'message': 'เซพซิสคืออะไร'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['found'])
        self.assertIn('ภาวะเซพซิสคืออะไร?', response.data['faq']['question'])
