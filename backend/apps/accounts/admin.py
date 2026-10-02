from django.contrib import admin
from .models import FamilyGroup, LineUser

class LineUserInline(admin.TabularInline):
    model = LineUser
    extra = 0
    fields = ('name', 'role', 'id_card', 'age', 'underlying_disease', 'is_registered')
    readonly_fields = ('registered_at',)

@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'get_members_count', 'get_patient_name', 'get_caregiver_name', 'created_at')
    search_fields = ('code', 'members__name', 'members__id_card')
    inlines = [LineUserInline]

    def get_members_count(self, obj):
        return obj.members.count()
    get_members_count.short_description = 'จำนวนสมาชิก'

    def get_patient_name(self, obj):
        patient = obj.members.filter(role='patient').first()
        return patient.name if patient else '-'
    get_patient_name.short_description = 'ชื่อผู้ป่วย'

    def get_caregiver_name(self, obj):
        caregiver = obj.members.filter(role='caregiver').first()
        return caregiver.name if caregiver else '-'
    get_caregiver_name.short_description = 'ชื่อผู้ดูแล'


@admin.register(LineUser)
class LineUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'family_code', 'id_card', 'age', 'underlying_disease', 'is_registered', 'registered_at')
    list_filter = ('role', 'is_registered', 'registered_at')
    search_fields = ('name', 'id_card', 'line_user_id', 'display_name', 'underlying_disease')
    list_editable = ('underlying_disease',)
    fieldsets = (
        ('ข้อมูลสิทธิและการเชื่อมต่อ LINE', {
            'fields': ('line_user_id', 'display_name', 'is_registered', 'registered_at')
        }),
        ('ข้อมูลส่วนตัวผู้ป่วย / ผู้ดูแล', {
            'fields': ('name', 'id_card', 'age', 'role', 'family')
        }),
        ('ข้อมูลการแพทย์ (สำหรับพยาบาล/แพทย์บันทึก)', {
            'fields': ('underlying_disease', 'allergy'),
            'description': 'กรอกหรือแก้ไขข้อมูลโรคประจำตัวและประวัติการแพ้ยาของผู้ป่วย ณ จุดนี้'
        }),
    )
    readonly_fields = ('registered_at',)

    def family_code(self, obj):
        return obj.family.code if obj.family else '-'
    family_code.short_description = 'รหัสครอบครัว'
