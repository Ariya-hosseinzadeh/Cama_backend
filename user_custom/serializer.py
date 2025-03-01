import attrs
from rest_framework import serializers, status
from rest_framework.response import Response

from user_custom.models import CustomUser, AdditionalInformationUser, Skills, Employee
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields = ['username', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class AgainSendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        # NationalCode = attrs.get('NationalCode')
        user_custom = CustomUser.objects.filter(email=email).first()
        if not user_custom:
            raise serializers.ValidationError('invalid user')
        return attrs

class RecoverypaaswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


    def validate(self, attrs):
        email = attrs.get('email')
        NationalCode = attrs.get('NationalCode')
        user_custom = CustomUser.objects.filter(NationalCode=NationalCode, email=email).first()
        if not user_custom:
            raise serializers.ValidationError('invalid NationalCode')
        return attrs

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}  # رمز عبور در پاسخ API نمایش داده نشود

        def validate_password(self, value):
            """اعتبارسنجی رمز عبور با regex"""
            if len(value) < 8:
                raise serializers.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
            if not re.search(r"[A-Z]", value):
                raise serializers.ValidationError("رمز عبور باید حداقل یک حرف بزرگ داشته باشد.")
            if not re.search(r"[a-z]", value):
                raise serializers.ValidationError("رمز عبور باید حداقل یک حرف کوچک داشته باشد.")
            if not re.search(r"\d", value):
                raise serializers.ValidationError("رمز عبور باید حداقل یک عدد داشته باشد.")
            if not re.search(r"[@$!%*?&]", value):
                raise serializers.ValidationError("رمز عبور باید حداقل یک کاراکتر خاص داشته باشد (!@#$%^&*...).")
            return value
class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model =AdditionalInformationUser
        fields ='__all__'

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Skills
        fields ='__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Employee
        fields ='__all__'