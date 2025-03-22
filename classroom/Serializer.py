from datetime import datetime

from django.template.defaultfilters import title
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from PIL import Image
import os

from twisted.conch.manhole import CTRL_E
from twisted.mail.scripts.mailmail import senderror

from Dashboard.models import Notification
from classroom.models import  *
from user_custom.models import CustomUser



# from classroom.views import DetailRequest


class CreateRequestClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        exclude = ('is_active','CodeCreator','LinkAccess','username')
        extra_kwargs = {


        }
    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        course=CourseRequest.objects.filter(Title=attr['Title'],description=attr['description'],is_active=True,CountClass=attr['CountClass'],category=attr['category'])
        if course:
            raise ValidationError({'Repetition':'کلاس شما قبلا ثبت شده است'})

        SuggestedTime = attr.get('SuggestedTime')

        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError({'SuggestedTime':f"زمان نمیتواند از زمان اکنون کمتر باشد"})
        category = attr['category']
        if category is None or category not in Category.objects.all():
            raise ValidationError({'category':'خطا در دسته بندی لطفا دسته بندی را درست وارد کنید '})
        return attr
class DetailCourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =CourseCreate
        exclude = ( 'is_active',)
        extra_kwargs = {
            'Creator':{'read_only':True},
            'CodeCreator':{'read_only':True},
            'username':{'read_only':True},
            'LinkAccess':{'read_only':True},
            'Title':{'read_only':True},
            'images':{'read_only':True},
            'category':{'read_only':True},
        }


    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        # course=CourseRequest.objects.filter(Title=attr['Title'],description=attr['description'],is_active=True,CountClass=attr['CountClass'],category=attr['category'])

        SuggestedTime = attr.get('SuggestedTime')

        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError(f"زمان نمیتواند از زمان اکنون کمتر باشد")
        return attr
class DetailCourseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model =CourseRequest
        exclude = (  'is_active',)
        extra_kwargs = {
            'Creator':{'read_only':True},
            'CodeCreator':{'read_only':True},
            'username':{'read_only':True},
            'LinkAccess':{'read_only':True},
            'Title':{'read_only':True},
            'category':{'read_only':True},
            'accepted_teacher':{'read_only':True},
        }


    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        # course=CourseRequest.objects.filter(Title=attr['Title'],description=attr['description'],is_active=True,CountClass=attr['CountClass'],category=attr['category'])

        SuggestedTime = attr.get('SuggestedTime')

        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError(f"زمان نمیتواند از زمان اکنون کمتر باشد")
        return attr
    # def create(self, validated_attr):
    #     request = self.context.get('request')
    #     validated_attr['Creator'] = request.user
    #     return super().create(validated_attr) در نسخه اصلی اضافه شود
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
    # def create(self, validated_attr):
    #     request = self.context.get('request')
    #     validated_attr['Creator'] = request.user
    #     return super().create(validated_attr) در نسخه اصلی اضافه شود


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
       ,'response':{'read_only': True},
            'status':{'read_only': True},

        }
    def validate(self, attr):
        try:
            teacher_code = attr.pop('teacher_code')  # مقدار را بردار و حذف کن
            teacher = CustomUser.objects.get(codeUser=teacher_code)
            attr['teacher'] = teacher

            #creator = self.context.get('request').attr.get('creator')#user
            #course=self.context.get('id')
        except CustomUser.DoesNotExist:
            raise ValidationError('کد کاربری نادرست است')
        course =attr.get('course_request')
        if CourseInvitation.objects.filter(course_request=course,teacher=teacher).exists():
            raise ValidationError('شما قبلا از این استاد برای این کلاستان دعوت کرده اید')
        print(CourseInvitation.objects.filter(course_request=course,teacher=teacher).exists())
        print(attr)
        return attr

    def create(self, validated_attr):
        return super().create(validated_attr)

# این سریالایزر برای دانشجو است تا دعوت هایی که کرده است را تغییر دهد
class InventationStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInvitation
        fields='__all__'
        extra_kwargs = {
            'status':{
                'read_only': True,

            },
            'teacher':{
                'read_only': True,
            },
            'course_request':{
                'read_only': True,
            },
            'response':{
                'read_only': True,
            }
        }
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProposalRequestCourse
        exclude=( 'status','user')
        extra_kwargs = {
            'user':{'read_only':True},



        }
    # def create(self, validated_attr):
    #
    # #     request = self.context.get('request')
    # #     validated_attr['user'] = request.user
    # #     return super().create(validated_attr)
    # #  فرستادن اعلان برای یک پیشنهاد
    #
    #     price = validated_attr.get('price')
    #     message = validated_attr.get('message')
    #     is_agreement = validated_attr.get('is_agreement')
    #
    #     print(validated_attr.get('course'),message,is_agreement,price)
        # description = f'برای کلاس {validated_attr.get('course').Title}\nprice:{price},\nmessage:{message},\nprice_agreement:{is_agreement}یک پیشنهاد دارید:'
        # sender = self.context.get('request').attr.get('user')#.userتغییر کند
        # user = self.context.get('request').attr.get('course').Creator
        # title=validated_attr.get('course').Title
        # notification=Notification.objects.create(user=user,sender=sender,title=title,description=description)
        #super().create(validated_attr)
        
        
    

    
    def update(self, instance, validated_attr):
        old_status = instance.price
        old_response=instance.message
        instance.price=validated_attr['price']
        instance.message=validated_attr['message']
        instance.save()
        changes = []
        if old_status != instance.status:
            changes.append({f'یپیشنهاد شما به {instance.price}تغییر یافته است'})
        if old_response != instance.response:
            changes.append(f'{instance.message}پیشنهاد شما یک پاسخ دارد:')
        if changes:
            description=f'پیشنهاد کلاس {instance.course.Title} به {instance.status} تغییر یافت. \n پاسخ پیشنهاد شما :{instance.response}'
            user=instance.course.Creator
            sender=instance.user
            title=instance.course.Title
            notification=Notification.objects.create(user=user,sender=sender,title=title,description=description)
        return instance
class propsalResponse(serializers.ModelSerializer):
    class Meta:
        model=ProposalRequestCourse
        exclude=( 'message','price')
        extra_kwargs = {
            'user': {'read_only': True},
            'message': {'read_only': True},
            'price': {'read_only': True},
        }
    def update(self, instance, validated_attr):
        old_status = instance.status
        old_response=instance.response
        instance.status=validated_attr['status']
        instance.response=validated_attr['response']
        instance.save()
        changes = []
        if old_status != instance.status:
            changes.append({f'یپیشنهاد شما به {instance.status}تغییر یافته است'})
        if old_response != instance.response:
            changes.append(f'{instance.response}پیشنهاد شما یک پاسخ دارد:')
        if changes:
            description=f'پیشنهاد کلاس {instance.course.Title} به {instance.status} تغییر یافت. \n پاسخ پیشنهاد شما :{instance.response}'
            user=instance.user
            sender=instance.course.Creator
            title=instance.course.Title
            notification=Notification.objects.create(user=user,sender=sender,title=title,description=description)
        return instance
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
        fields='__all__'
        extra_kwargs = {
            'Creator':{'write_only': True},
            'is_active':{'read_only':True},
            'CodeCreator':{'read_only':True},
            'username':{'read_only':True},
            'LinkAccess':{'read_only':True},

        }
    def validate(self, attr):

        images=attr.get('images')
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
        user=self.context.get('request').user
        course = CourseCreate.objects.filter(Creator=user,Title=attr['Title'], description=attr['description'], is_active=True, category=attr['category'])
        if course:
            raise ValidationError({'Repetition':'کلاس شما قبلا ثبت شده است'})
        SuggestedTime = attr.get('SuggestedTime')
        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError({'SuggestedTime':f"زمان نمیتواند از زمان اکنون کمتر باشد"})
        category = attr['category']
        if category is None or category not in Category.objects.all():
            raise ValidationError({'category': 'خطا در دسته بندی لطفا دسته بندی را درست وارد کنید '})
        return attr
    def create(self, validated_attr):
        request=self.context.get('request')
        validated_attr['Creator'] = request.user
        print(validated_attr['Creator'])
        return super().create(validated_attr)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AgreementCourseRequest
        fields='__all__'
class AgreementCourseRequsetSerializer(serializers.ModelSerializer):
    pass
class ResponseIventationTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInvitation
        fields='__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'description': {'read_only': True},
            'course_request': {'read_only': True},
            'creator': {'read_only': True},
        }
