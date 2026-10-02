from django.urls import path
from .views import FAQListView, FAQSearchEngine

urlpatterns = [
    path('list/', FAQListView.as_view(), name='faq-list'),
    path('search/', FAQSearchEngine.as_view(), name='faq-search'),
]
