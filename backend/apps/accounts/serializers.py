from rest_framework import serializers
from .models import FamilyGroup, LineUser

class LineUserSerializer(serializers.ModelSerializer):
    family_code = serializers.CharField(source='family.code', read_only=True)

    class Meta:
        model = LineUser
        fields = [
            'id', 'line_user_id', 'display_name', 'name', 'id_card', 'phone_number',
            'age', 'role', 'family', 'family_code', 'is_registered', 
            'registered_at', 'underlying_disease', 'allergy'
        ]
        read_only_fields = ['id', 'is_registered', 'registered_at', 'underlying_disease']


class RegisterSerializer(serializers.Serializer):
    line_user_id = serializers.CharField(max_length=50)
    display_name = serializers.CharField(max_length=100, required=False, default='')
    name = serializers.CharField(max_length=100)
    id_card = serializers.CharField(max_length=13)
    phone_number = serializers.CharField(max_length=15)
    age = serializers.IntegerField(min_value=1)
    role = serializers.ChoiceField(choices=['patient', 'caregiver', 'nurse'])
    family_code = serializers.CharField(max_length=10, required=False, allow_blank=True, default='')

    def validate_id_card(self, value):
        if not value.isdigit() or len(value) != 13:
            raise serializers.ValidationError("เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก")
        return value

    def validate_phone_number(self, value):
        cleaned = value.replace('-', '').replace(' ', '')
        if not cleaned.isdigit() or len(cleaned) < 9 or len(cleaned) > 10:
            raise serializers.ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-10 หลัก")
        return cleaned
