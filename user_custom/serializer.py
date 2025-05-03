import os
from datetime import date,timedelta

import attrs

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from user_custom.models import CustomUser, AdditionalInformationUser, Skills, Employee, City, Province, UserSkill, \
    CareerHistory, Job
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

        user_custom = CustomUser.objects.filter(email=email).first()
        if not user_custom:
            raise serializers.ValidationError({'error_message': 'invalid user'})
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

        extra_kwargs = {"user": {"read_only": True},
                        "profile_image":{"read_only": True}
                        }

    def validate(self, attr):

        birth_date = attr.get('birth_date')
        if birth_date:
            min_age = 8
            today = date.today()
            min_birth_date = date(today.year - min_age, today.month, today.day)

            if birth_date > min_birth_date:
                raise ValidationError({'ageError':f"سن شما باید حداقل {min_age} سال باشد."})
        else:
            raise ValidationError({'birth-date':'تاریخ تولد تعیین نشده است'})

        bio = attr.get('bio')
        if bio:
            bio = bio.strip()
            if len(bio) != 0 and len(bio.strip()) < 30:
                raise ValidationError({'status': 'بیوگرافی شما از 30 کاراکتر نمیتواند کمتر باشد'})

        # images = attr.get('profile_image')
        # if images is None:
        #     raise ValidationError('عکسی بارگذاری نشده است')
        # max_size = 5 * 1024 * 1024  # 5MB
        # if images.size > max_size:
        #     raise ValidationError({'images': "حجم تصویر نباید بیشتر از ۵ مگابایت باشد."})
        #
        # # بررسی فرمت تصویر
        # allowed_extensions = ["jpg", "jpeg", "png"]
        # ext = os.path.splitext(images.name)[1][1:].lower()
        # if ext not in allowed_extensions:
        #     raise ValidationError({'images': "فرمت تصویر باید JPEG یا PNG باشد."})
        #     # بررسی ابعاد تصویر
        # img = Image.open(images)
        # min_width, min_height = 300, 300
        # if img.width < min_width or img.height < min_height:
        #     raise ValidationError({'images': f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد."})
        return attr




class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Employee
        fields ='__all__'
from PIL import Image
class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =AdditionalInformationUser
        fields =['profile_image','user']
        extra_kwargs = {"user": {"read_only": True}}
    def validate(self, attr):
        images=attr.get('profile_image')
        if images is None:
            raise ValidationError('عکسی بارگذاری نشده است')
        max_size = 5 * 1024 * 1024  # 5MB
        if images.size > max_size:
            raise ValidationError({'images':"حجم تصویر نباید بیشتر از ۵ مگابایت باشد."})

        # بررسی فرمت تصویر
        allowed_extensions = ["jpg", "jpeg", "png"]
        ext = os.path.splitext(images.name)[1][1:].lower()
        if ext not in allowed_extensions:
            raise ValidationError({'images':"فرمت تصویر باید JPEG یا PNG باشد."})
            # بررسی ابعاد تصویر
        img = Image.open(images)
        min_width, min_height = 300, 300
        if img.width < min_width or img.height < min_height:
            raise ValidationError({'images':f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد."})
        return attr
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Province
        fields ='__all__'
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields ='__all__'
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Skills
        fields=['name','id']
class UserSkillSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'level', 'user','title']
        read_only_fields = ['user','title']
    def get_title(self, obj):
        return f"{obj.skill.name}: {obj.level}"

class CareerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerHistory
        fields = ['id','user_data','job','company','date_start','date_end','NowBusy']

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields ='__all__'
    # def create(self, validated_data):
    #     # user = self.context['request'].user
    #     user=CustomUser.objects.get(id=1)
    #     validated_data['user'] = user.additional_info
    #     return super().create(validated_data)
