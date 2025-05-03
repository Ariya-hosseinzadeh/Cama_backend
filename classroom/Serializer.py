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
            'teacher_rating':{'read_only':True},
            'category':{'read_only':True},
            'enrolled_students':{'read_only':True},
            'images':{'read_only':True},
        }

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user != instance.Creator:
            raise ValidationError(
                {'message_error': 'شما نمیتوانید بر روی کلاس دیگران تغییرات لحاظ کنید.\nاگر وارد نشدید وارد شوید'})

        # سایر فیلدها به‌روزرسانی شوند
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        # course=CourseRequest.objects.filter(Title=attr['Title'],description=attr['description'],is_active=True,CountClass=attr['CountClass'],category=attr['category'])
        images = attr.get('images')
        if images:
            max_size = 5 * 1024 * 1024  # 5MB
            if images.size > max_size:
                raise ValidationError({"error_message":"حجم تصویر نباید بیشتر از ۵ مگابایت باشد."})

            # بررسی فرمت تصویر
            allowed_extensions = ["jpg", "jpeg", "png"]
            ext = os.path.splitext(images.name)[1][1:].lower()
            if ext not in allowed_extensions:
                raise ValidationError({"error_message": "فرمت تصویر باید JPEG یا PNG باشد."})

            # بررسی ابعاد تصویر
            img = Image.open(images)
            min_width, min_height = 300, 300
            if img.width < min_width or img.height < min_height:
                raise ValidationError({'error_message':f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد."})
        SuggestedTime = attr.get('SuggestedTime')

        now = timezone.now()
        if SuggestedTime < now:
            raise ValidationError({"error_message":f"زمان نمیتواند از زمان اکنون کمتر باشد"})
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PUT':
            self.fields.pop('images', None)  # حذف فیلد از serializer


    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user != instance.Creator:
            raise ValidationError(
                {'message_error': 'شما نمیتوانید بر روی کلاس دیگران تغییرات لحاظ کنید.\nاگر وارد نشدید وارد شوید'})

        # سایر فیلدها به‌روزرسانی شوند
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    # def delete(self, instance, validated_data):
    #     user = self.context['request'].user
    #     if user != instance.Creator:
    #         raise ValidationError({'error_message':'لطفا وارد شوید'})
    #     instance.delete()در جنگو رست نمیتوان در سریالایز متد  حذف را تعریف کرد

    def validate(self, attr):
        """ بررسی اندازه، فرمت و ابعاد تصویر قبل از ذخیره """

        images = attr.get('images')
        SuggestedTime = attr.get('SuggestedTime')
        if images:
            max_size = 5 * 1024 * 1024  # 5MB
            if images.size > max_size:
                raise ValidationError({"error_message":"حجم تصویر نباید بیشتر از ۵ مگابایت باشد."})

            # بررسی فرمت تصویر
            allowed_extensions = ["jpg", "jpeg", "png"]
            ext = os.path.splitext(images.name)[1][1:].lower()
            if ext not in allowed_extensions:
                raise ValidationError({"error_message": "فرمت تصویر باید JPEG یا PNG باشد."})

            # بررسی ابعاد تصویر
            img = Image.open(images)
            min_width, min_height = 300, 300
            if img.width < min_width or img.height < min_height:
                raise ValidationError({'error_message':f"ابعاد تصویر نباید کمتر از {min_width}x{min_height} پیکسل باشد."})

        now = timezone.now()
        if SuggestedTime is None:
            raise ValidationError({'error_message':'لطفا زمان را تعیین کنید'})
        if SuggestedTime < now:
            raise ValidationError({'error_message':"زمان نمیتواند از زمان اکنون کمتر باشد"})


        return attr



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
            }
       ,'response':{'read_only': True},
            'status':{'read_only': True},
            'course_request':{'read_only': True},
            'creator':{'read_only': True},

        }

    def validate(self, attr):
        try:
            teacher_code = attr.pop('teacher_code')  # مقدار را بردار و حذف کن
            teacher = CustomUser.objects.get(codeUser=teacher_code)
            attr['teacher'] = teacher

        except CustomUser.DoesNotExist:
            raise ValidationError({'error_message':'کد کاربری نادرست است'})
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            raise ValidationError({'error_message': 'Not Authenticated'})
        attr['creator'] = user

        course_id=self.context.get('id')
        course = CourseRequest.objects.filter(id=course_id).first()
        if not course:
            raise ValidationError({'error_message': 'کلاس مورد نظر یافت نشد'})

        if CourseInvitation.objects.filter(course_request=course,teacher=teacher).exists():
            raise ValidationError({'error_message':'شما قبلا از این استاد برای این کلاستان دعوت کرده اید'})

        return attr

    def create(self, validated_attr):
        validated_attr['course_request']=CourseRequest.objects.filter(id=self.context.get('id')).first()

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
            },
            'creator':{'read_only': True},
            'code_teacher':{'read_only': True},
            'code_Creator':{'read_only': True},
            'Course_name':{'read_only': True},
            'teacher_name':{'read_only': True},
            'creator_name':{'read_only': True},
        }
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProposalRequestCourse
        fields='__all__'
        extra_kwargs = {
            'user_proposal':{'read_only':True},
            'status':{
                'read_only': True,},
            'response':{
                'read_only': True,

            },
            'Creator':{'read_only':True},
            'created_at':{'read_only':True},

            'course_request':{'read_only':True},


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
    
    # def update(self, instance, validated_attr):
    #     old_status = instance.price
    #     old_response=instance.message
    #     instance.price=validated_attr['price']
    #     instance.message=validated_attr['message']
    #     instance.save()
    #     changes = []
    #     if old_status != instance.status:
    #         changes.append({f'یپیشنهاد شما به {instance.price}تغییر یافته است'})
    #     if old_response != instance.response:
    #         changes.append(f'{instance.message}پیشنهاد شما یک پاسخ دارد:')
    #     if changes:
    #         description=f'پیشنهاد کلاس {instance.course.Title} به {instance.status} تغییر یافت. \n پاسخ پیشنهاد شما :{instance.response}'
    #         user=instance.course.Creator
    #         sender=instance.user
    #         title=instance.course.Title
    #         notification=Notification.objects.create(user=user,sender=sender,title=title,description=description)
    #     return instance
class propsalResponse(serializers.ModelSerializer):
    class Meta:
        model=ProposalRequestCourse
        fields=['price','response','course_request','user_proposal','status']
        # def is_agreement:
        #     proposal=ProposalRequestCourse.objects.filter(course=)
        extra_kwargs = {
            'user_proposal': {'read_only': True},
            'course_request': {'read_only': True},
        }
    def update(self, instance, validated_attr):
        old_status = instance.status
        old_response=instance.response
        # old_price=instance.price
        instance.status=validated_attr['status']
        instance.response=validated_attr['response']
        # instance.price=validated_attr['price']
        instance.save()
        changes = []
        if old_status != instance.status:
            changes.append({f'یپیشنهاد شما به {instance.status}تغییر یافته است'})
        # if old_price != instance.price:
        #     changes.append({f'قیمت کلاس شما به {instance.price}تغییر یافت در صفحه شخصی تان میتوانید بپذیرید یا رد کنید'})
        if old_response != instance.response:
            changes.append(f'{instance.response}پیشنهاد شما یک پاسخ دارد:')
        if changes:
            description=f'پیشنهاد کلاس {instance.course_request.Title} به {instance.status} تغییر یافت. \n پاسخ پیشنهاد شما :{instance.response}'
            user=instance.user_proposal
            sender=instance.course_request.Creator
            title=instance.course_request.Title
            notification=Notification.objects.create(user=user,sender=sender,title=title,description=description)
        return instance

class RegisteringCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCreate
        fields = ['enrolled_students', 'Creator', 'CapacityCourse']
        extra_kwargs = {
            'Creator': {'read_only': True},
            'CapacityCourse': {'read_only': True},
            'enrolled_students': {'read_only': True},
        }

    def validate(self, attrs):
        course = self.instance
        user = self.context['request'].user
        if not user or not user.is_authenticated:
            raise ValidationError({'NotAuth':"ابتدا وارد حساب کاربری خود شوید."})
        # آیا کاربر قبلاً ثبت‌نام کرده؟
        if course.enrolled_students.filter(id=user.id).exists():
            raise ValidationError({'registering':'شما قبلاً در این دوره ثبت‌نام کرده‌اید.'})

        # بررسی ظرفیت
        if course.enrolled_students.count() >= course.CapacityCourse:
            raise ValidationError({'Capacity':"ظرفیت کلاس تکمیل شده است."})

        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.enrolled_students.add(user)
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
            'code_Creator': {'read_only': True},
            'code_teacher': {'read_only': True},
            'Course_name': {'read_only': True},
            'creator_name': {'read_only': True},
            'teacher_name': {'read_only': True},
            'teacher':{'read_only': True},
        }

class myCourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=CourseCreate
        fields=['id','username','Creator','Title','description','images','category',]
        extra_kwargs = {
            'username': {'read_only': True},
            'Creator': {'read_only': True},
            'category': {'read_only': True},
            'id': {'read_only': True},
        }

    def validate(self, attr):
            pass
class myCouseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseRequest
        fields=['username','Creator','Title','description','category','images','id']
        extra_kwargs = {
            'username': {'read_only': True},
            'Creator': {'read_only': True},
            'id':{'read_only': True},
        }