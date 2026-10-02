from rest_framework import serializers
from .models import VitalSign

class VitalSignSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = VitalSign
        fields = '__all__'
        read_only_fields = ['id', 'recorded_at']

    def validate_temperature(self, value):
        if value is not None and (value < 30.0 or value > 45.0):
            raise serializers.ValidationError("อุณหภูมิกายต้องอยู่ระหว่าง 30.0 ถึง 45.0 °C")
        return value

    def validate_spo2(self, value):
        if value is not None and (value < 50 or value > 100):
            raise serializers.ValidationError("ค่า SpO2 ต้องอยู่ระหว่าง 50% ถึง 100%")
        return value
