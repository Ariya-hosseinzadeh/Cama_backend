from datetime import datetime
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from PIL import Image
import os
from classroom.models import  *
from user_custom.models import CustomUser


# from classroom.views import DetailRequest


class CreateRequestClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest

        exclude = ('LinkAccess','accepted_teacher','Creator','is_active')
        # extra_kwargs = {
        #     'Creator': {'read_only': True}
        # }

class DetailCourseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        exclude = ( 'accepted_teacher',  'is_active')



    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        course=CourseRequest.objects.filter(Title=attr['Title'],description=attr['description'],is_active=True,CountClass=attr['CountClass'],category=attr['category'])
        if course:
            raise ValidationError('کلاس شما قبلا ثبت شده است')

        SuggestedTime = attr.get('SuggestedTime')

        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError(f"زمان نمیتواند از زمان اکنون کمتر باشد")
        return attr
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['Creator'] = request.user
    #     return super().create(validated_data) در نسخه اصلی اضافه شود
    # def validate(self, attr):
    #     """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """
    #     images = attr.get('images')
    #     SuggestedTime = attr.get('SuggestedTime')
    #     max_size = 5 * 1024 * 1024  # 5MB
    #     if images.size > max_size:
    #         raise ValidationError("حجم تصویر نباید بیشتر از ۵ مگابایت باشد.")
    #
    #     # بررسی فرمت تصویر
    #     allowed_extensions = ["jpg", "jpeg", "png"]
    #     ext = os.path.splitext(images.name)[1][1:].lower()
    #     if ext not in allowed_extensions:
    #         raise ValidationError("فرمت تصویر باید JPEG یا PNG باشد.")
    #
    #     # بررسی ابعاد تصویر
    #     img = Image.open(images)
    #     min_width, min_height = 300, 300
    #     if img.width < min_width or img.height < min_height:
    #         raise ValidationError(f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد.")
    #
    #     now = timezone.now()
    #     if SuggestedTime < now:
    #         raise ValidationError(f"زمان نمیتواند از زمان اکنون کمتر باشد")
    #     return attr
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['Creator'] = request.user
    #     return super().create(validated_data) در نسخه اصلی اضافه شود


class HallWaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model=WaitingHall
        fields='__all__'

class InventiationTeacherSerializer(serializers.ModelSerializer):
    teacher_code=serializers.CharField(max_length=12,write_only=True)
    class Meta:
        model=CourseInvitation
        fields='__all__'
        extra_kwargs = {
            'teacher':{
                'read_only': True,
            }#یوزر ایجاد کننده هم باید از رکوئست گرفته شود
        }
    def validate(self, attr):
        try:
            teacher_code = attr.pop('teacher_code')  # مقدار را بردار و حذف کن
            teacher = CustomUser.objects.get(codeUser=teacher_code)
            attr['teacher'] = teacher

            #creator = self.context.get('request').data.get('creator')#user
            #course=self.context.get('id')
        except CustomUser.DoesNotExist:
            raise ValidationError('کد کاربری نادرست است')
        course =self.context.get('request').data.get('course_request')
        if CourseInvitation.objects.filter(course_request=course,teacher=teacher).exists():
            raise ValidationError('شما قبلا از این استاد برای این کلاستان دعوت کرده اید')
        return attr

    def create(self, validated_data):
        return super().create(validated_data)


class InventationStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInvitation
        fields='__all__'
        extra_kwargs = {
            'status':{
                'read_only': True,
            }
        }
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proposal
        exclude=( 'status','user',)
    #     extra_kwargs = {
    #         'user':{'read_only':True},
    #     }
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['user'] = request.user
    #     return super().create(validated_data)
# class ListCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ListMyClasses
#         fields = '__all__'

# class ProposalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Proposal
#         fields = '__all__'
# # class AcceptingSerializer(serializers.Serializer):
# #     requestsid=serializers
# #     waiting=HallWaiting
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseCreate
        exclude = ('LinkAccess','Creator')
        # extra_kwargs = {
        #     'Creator':{'read_only':True}
        # }
        def validatedata(self, data):
            """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """
            images=data.get('images')
            SuggestedTime=data.get('SuggestedTime')
            max_size = 5 * 1024 * 1024  # 5MB
            if images.size > max_size:
                raise ValidationError("حجم تصویر نباید بیشتر از ۵ مگابایت باشد.")

            # بررسی فرمت تصویر
            allowed_extensions = ["jpg", "jpeg", "png"]
            ext = os.path.splitext(images.name)[1][1:].lower()
            if ext not in allowed_extensions:
                raise ValidationError("فرمت تصویر باید JPEG یا PNG باشد.")

            # بررسی ابعاد تصویر
            img = Image.open(images)
            min_width, min_height = 300, 300
            if img.width < min_width or img.height < min_height:
                raise ValidationError(f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد.")

            now = timezone.now()
            if SuggestedTime < now:
                raise ValidationError(f"زمان نمیتواند از زمان اکنون کمتر باشد")
            return data

        # def create(self, validated_data):
        #     request=self.context.get('requests')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AgreementCourseRequest
        fields='__all__'

