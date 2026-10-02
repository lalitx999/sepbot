from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import FAQ
from .serializers import FAQSerializer

class FAQListView(APIView):
    """
    List or Search FAQ 33 questions
    """
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        category = request.query_params.get('category', '').strip()

        faqs = FAQ.objects.all()
        if category:
            faqs = faqs.filter(category=category)

        if query:
            faqs = faqs.filter(
                Q(question__icontains=query) | Q(answer__icontains=query)
            )

        return Response(FAQSerializer(faqs, many=True).data)


class FAQSearchEngine(APIView):
    """
    Keyword Matcher for LINE Chatbot queries
    """
    def post(self, request):
        user_message = request.data.get('message', '').strip()
        if not user_message:
            return Response({'found': False, 'message': 'กรุณาระบุข้อความที่ต้องการค้นหา'})

        # Find best matching FAQ
        matched_faq = FAQ.objects.filter(
            Q(question__icontains=user_message) | Q(answer__icontains=user_message)
        ).first()

        if matched_faq:
            return Response({
                'found': True,
                'faq': FAQSerializer(matched_faq).data
            })
        
        return Response({
            'found': False,
            'message': 'ไม่พบคำตอบอัตโนมัติสำหรับคำถามนี้ กรุณากดปุ่ม "ติดต่อพยาบาล" เพื่อสอบถามทีมผู้ดูแลโดยตรงครับ'
        })
