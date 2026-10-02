from rest_framework import serializers
from .models import DailyCheck, SepsisScreening

class DailyCheckSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = DailyCheck
        fields = '__all__'
        read_only_fields = ['id', 'result_level', 'responded_at']


class SepsisScreeningSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = SepsisScreening
        fields = '__all__'
        read_only_fields = ['id', 'has_red_flag', 'has_amber_flag', 'result']
