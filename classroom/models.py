from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.authtoken.admin import User

from Rating.models import Rating, Comment
from Tags.models import Tag, Category
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
import os
import uuid

from user_custom.models import CustomUser


# Create your models here.
def generate_unique_link():
    return str(uuid.uuid4())[:18]

class CourseRequest(models.Model):
    LinkAccess=models.CharField(max_length=18,unique=True,default=generate_unique_link,blank=False,null=False)#لینک یکتا برای دسترسی به هر کلاس
    Creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='requester',null=False,db_index=True,default=1)
    username=models.CharField(max_length=18,null=False,blank=False)
    CodeCreator=models.CharField(max_length=18,null=False,blank=False)
    Title=models.CharField(max_length=200,db_index=True)
    description = models.TextField()
    CountClass = models.IntegerField(default=1)
    SuggestedTime = models.DateTimeField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses", db_index=True)
    #inviteUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calling', null=True, blank=True)
    accepted_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_teacher', null=True,blank=True)#این فیلد بصورت خودکار پر میشود
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    price_course = models.FloatField(null=True,blank=True)
    images=models.ImageField(null=True,blank=True)
    level_course = models.IntegerField(default=1, choices=[(1, 'elementary'), (3, 'intermediate'), (5, 'advanced')])
    def __str__(self):
        return f'{self.Creator} - {self.Title}'
    class Meta:
        verbose_name_plural = 'Class Requests'
        ordering = ['-SuggestedTime']

    def save(self, *args, **kwargs):
        """ فشرده‌سازی تصویر هنگام ذخیره """
        self.username = self.Creator.username
        self.CodeCreator = self.Creator.codeUser
        super().save(*args, **kwargs)
        img_path = self.images.path
        img = Image.open(img_path)
        # کاهش کیفیت تصویر بدون افت محسوس
        img = img.convert("RGB")  # اگر فرمت PNG باشد، به RGB تبدیل شود

        img.save(img_path, format="JPEG", quality=70, optimize=True)  # فشرده‌سازی


# ارور حداکثر تعداد کلاس ها در سریالایزر مدیریت میشود
class CourseCreate(models.Model):
    LinkAccess = models.CharField(max_length=18,unique=True,default=generate_unique_link,blank=False,null=False)
    Creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='creator',null=False,blank=False,db_index=True,default=1)
    username = models.CharField(max_length=18, null=False, blank=False)
    CodeCreator = models.CharField(max_length=18, null=False, blank=False)
    Title=models.CharField(max_length=200,db_index=True)
    description=models.TextField()
    CapacityCourse=models.IntegerField(default=1)
    CountClass = models.IntegerField(default=1)
    SuggestedTime = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="coursesCreate", db_index=True)
    images=models.ImageField(upload_to="media/courseImages", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_course = models.FloatField(null=True,blank=True)
    level_course = models.IntegerField(default=1, choices=[(1, 'elementary'), (3, 'intermediate'), (5, 'advanced')])
    enrolled_students=models.ManyToManyField(CustomUser,related_name='enrolled_students',blank=True,null=True)
    teacher_rating = models.FloatField(default=0)
    def save(self, *args, **kwargs):
        """ فشرده‌سازی تصویر هنگام ذخیره """
        self.username = self.Creator.username
        self.CodeCreator = self.Creator.codeUser
        super().save(*args, **kwargs)
        img_path = self.images.path
        img = Image.open(img_path)
        # کاهش کیفیت تصویر بدون افت محسوس
        img = img.convert("RGB")  # اگر فرمت PNG باشد، به RGB تبدیل شود

        img.save(img_path, format="JPEG", quality=70, optimize=True)  # فشرده‌سازی

    def __str__(self):
        return f'{self.Creator} - {self.Title}'

#کلاس هایی که درخواست کننده ایجاد میکند در صورت تایید از تالار انتظار حذف و به اینجا اضافه میشود
class AgreementCourseRequest(models.Model):
    requestCourse = models.OneToOneField(CourseRequest, on_delete=models.CASCADE, related_name='requestCourse')
    Time=models.DateTimeField()

    #ClassLink=models.CharField(max_length=500,null=True,blank=True)
    #isHeld=models.BooleanField(default=False)
    #isCompleted=models.BooleanField(default=False)#تعیین میکند تمام جلسات کلاس برگزار شده است
    average_rating = models.FloatField(default=0.0)  # میانگین امتیاز
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="teacher_invent")
    student=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="creator_classRequest")
    comments = GenericRelation(Comment)

    def save(self, *args, **kwargs):
        self.teacher=self.requestCourse.accepted_teacher
        self.student=self.requestCourse.Creator
        super().save(*args, **kwargs)
    def update_average_rating(self):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        ratings = Rating.objects.filter(content_type=content_type, object_id=self.id)
        avg = ratings.aggregate(models.Avg('score'))['score__avg']
        self.average_rating = avg if avg else 0
        self.save()
# برای اینکه بررسی کنیم کاربر در کلاس حضور داشته یا نه!مثلا برای نمره دهی استاد باید حتما در کلاس باشد
    def has_student(self, user):
        return self.students.filter(id=user.id).exists()
    def __str__(self):
        return f'{self.requestCourse} - {self.ClassLink}'
    class Meta:
        verbose_name_plural = 'Agreement Course Requests'
        ordering = ['-Time']


#بقیه دانش آموزان باید توسط استاد اضافه شوند
class AgreementCourseCreate(models.Model):
    createCourse = models.OneToOneField(CourseCreate, on_delete=models.CASCADE, related_name='teacher_create')
    Time = models.DateTimeField()
    # ClassLink = models.CharField(max_length=500)#api از وبینار که گرفتیم پر میشود
    # is_Held = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0.0)  # میانگین امتیاز
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_course")
    students = models.ManyToManyField(User, related_name='students_attention', )
    comments = GenericRelation(Comment)


    def save(self, *args, **kwargs):
        self.teacher=self.createCourse.Creator
        self .students=self.createCourse.enrolled_students
        super().save(*args, **kwargs)
    def update_average_rating(self):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        ratings = Rating.objects.filter(content_type=content_type, object_id=self.id)
        avg = ratings.aggregate(models.Avg('score'))['score__avg']
        self.average_rating = avg if avg else 0
        self.save()
    # isCompleted=models.BooleanField(default=False)#تعیین میکند تمام جلسات کلاس برگزار شده است
        # برای اینکه بررسی کنیم کاربر در کلاس حضور داشته یا نه!مثلا برای نمره دهی استاد باید حتما در کلاس باشد
        def has_student(self, user):
            return self.students.filter(id=user.id).exists()
    def __str__(self):
        return f'{self.createCourse} - {self.ClassLink}'

    class Meta:
        verbose_name_plural = 'Agrement Course Create'
        ordering = ['-Time']


class WaitingHall(models.Model):
    # ClassRequest=models.OneToOneField(CourseRequest, on_delete=models.CASCADE,related_name='waititent',unique=True,null=False,blank=False)
    type_course =models.CharField(max_length=500)
    Title=models.CharField(max_length=200,db_index=True)
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # مدل مرتبط
    object_id = models.PositiveIntegerField()  # ID کلاس مرتبط
    ClassRequest = GenericForeignKey('content_type', 'object_id')  # ارتباط عمومی
    Creator=models.ForeignKey(User, on_delete=models.CASCADE, related_name="Creator")
    price=models.FloatField(default=0,null=True,blank=True)
    image=models.ImageField(upload_to="media/waitingHallImages", null=True, blank=True)
    CodeCreator=models.CharField(max_length=18,null=False,blank=False)

    def save(self, *args, **kwargs):
        self.Title=self.ClassRequest.Title
        self.description=self.ClassRequest.description
        self.price=self.ClassRequest.price_course
        self.Creator=self.ClassRequest.Creator
        self.CodeCreator=self.ClassRequest.CodeCreator
        self.image=self.ClassRequest.images
        self.type_course=self.content_type.model
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.ClassRequest.Title}is Attention by{self.ClassRequest.Creator}'


class CourseInvitation(models.Model):
    course_request = models.ForeignKey(CourseRequest, on_delete=models.CASCADE, related_name="invitations")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations")
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    response=models.TextField(blank=True)
    def save(self,*args, **kwargs):
        """اگر این استاد دعوت را بپذیرد، دیگر دعوت‌ها رد شوند و استاد در کلاس ثبت شود."""
        creator=self.course_request.Creator
        if(self.status== 'accepted'):
            self.course_request.accepted_teacher = self.teacher
            self.course_request.save()
            # CourseInvitation.objects.filter(course_request=self.course_request).exclude(id=self.id).update(
            #     status='rejected')
        super().save(*args, **kwargs)

#استاد میتواند بر روی یک کرات کلاس در تالار انتظار پیشنهاد دهد کاربر میتواند از کارت کلاس هایی که دارد ببیند بر روی کلاسش چه پیشنهاد هایی هست .اینطوری لازم نیست که کاربر برای اینکه بخواهد مقایسه کند پیشنهاد ها را لیستی از کلاس هارا مقایسه کند .پس ما در پیشنهاد های دانش آموز اینکه یصورت جامع تمام پیشنهاد هایش را یکجا ببیند قرار نخواهیم داد اما برای پیشنهاد دهنده وجود خواهد داشت
class ProposalRequestCourse(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در حال انتظار '),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده')

    )

    user_proposal = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    course_request=models.ForeignKey(CourseRequest, on_delete=models.CASCADE,related_name='proposals_Request')
    Creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Course_Creator')
    message = models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=10,)
    agreement_price=models.BooleanField(default=False)
    status = models.CharField(max_length=300,default='pending',choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.Creator=self.course_request.Creator
        if self.status == 'accepted':
            ProposalRequestCourse.objects.filter(course_request=self.course_request).exclude(id=self.id).update(
                status='rejected')
            CourseInvitation.objects.filter(course_request=self.course_request).update(
                status='rejected'
            )

        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Proposals_Request'
        ordering = ['-created_at']
class ProposalCreateCourse(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در حال انتظار '),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده')

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(CourseCreate, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=300,default='pending',choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = 'Proposals'
        ordering = ['-created_at']


        # تنظیم استاد در کلاس



        # رد کردن سایر دعوت‌ها




