from rest_framework import serializers
from .models import User
from django.core.cache import cache

class UserSerialzier(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if value[0:2] != "09":
            raise serializers.ValidationError("تلفن باید با 09 شروع شود", code="required")
        
            # raise serializers.ValidationError([serializers.ValidationError(
            #     "شماره تلفن نامعتبر است", code="invalid"), serializers.ValidationError("تلفن باید با 09 شروع شود", code="required")])
        # try:
        #     code = RGScode.objects.get(phone_number=value)
        #     code.delete()
        # except RGScode.DoesNotExist:
        #     pass
        return value
    


class UserVerifySerializer(serializers.Serializer):
    # phone_number = serializers.CharField(required=True)
    code = serializers.IntegerField()

    def validate_code(self,code):
        phone = cache.get(code,None)
        if len(str(code)) != 1:
            raise serializers.ValidationError("کد نامعتبر است.")
        elif not phone:
            raise serializers.ValidationError("کد وجود ندارد و یا منقضی شده")
        cache.delete_pattern(code)
        return phone