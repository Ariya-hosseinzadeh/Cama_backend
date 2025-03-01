from django.db import models
from rest_framework.authtoken.admin import User

from Tags.models import Tag, Category
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
import os
import uuid
# Create your models here.
def generate_unique_link():
    return str(uuid.uuid4())[:18]

class CourseRequest(models.Model):
    LinkAccess=models.CharField(max_length=18,unique=True,default=generate_unique_link,blank=False,null=False)#لینک یکتا برای دسترسی به هر کلاس
    Creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='requester',null=False,db_index=True,default=1)
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
    is_private=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.Creator} - {self.Title}'
    class Meta:
        verbose_name_plural = 'Class Requests'
        ordering = ['-SuggestedTime']
    def save(self, *args, **kwargs):
        self.username = self.Creator.username
        self.CodeCreator = self.Creator.codeUser
        super().save(*args, **kwargs)
# ارور حداکثر تعداد کلاس ها در سریالایزر مدیریت میشود
class CourseCreate(models.Model):
    LinkAccess = models.CharField(max_length=18, unique=True, default=str(uuid.uuid4())[:15], blank=False, null=False)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creator',null=False,blank=False,db_index=True,default=1)
    Title=models.CharField(max_length=200,db_index=True)
    description=models.TextField()
    #inviteUser=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    # applicants=models.ManyToManyField(User, related_name='applicants', blank=True)
    CapacityCourse=models.IntegerField(default=1,)
    CountClass = models.IntegerField(default=1)
    SuggestedTime = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="coursesCreate", db_index=True)
    images=models.ImageField(upload_to="media/courseImages", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        """ فشرده‌سازی تصویر هنگام ذخیره """
        super().save(*args, **kwargs)
        img_path = self.images.path
        img = Image.open(img_path)

        # کاهش کیفیت تصویر بدون افت محسوس
        img = img.convert("RGB")  # اگر فرمت PNG باشد، به RGB تبدیل شود
        img.save(img_path, format="JPEG", quality=70, optimize=True)  # فشرده‌سازی
    def __str__(self):
        return f'{self.Creator} - {self.Title}'
class GroupCourse(models.Model):#توسط دانشجو انجام میشود و هزینه را میتواند با توافق تایید کنند
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teachercourse")
    course = models.ForeignKey(CourseRequest, on_delete=models.CASCADE)
    Students=models.ManyToManyField(User, related_name='students',blank=True)
#کلاس هایی که درخواست کننده ایجاد میکند در صورت تایید از تالار انتظار حذف و به اینجا اضافه میشود
class AgreementCourseRequest(models.Model):
    requestCourse = models.OneToOneField(CourseRequest, on_delete=models.CASCADE, related_name='requestCourse')
    Time=models.DateTimeField()
    #CourseGroup=models.ForeignKey(GroupCourse, on_delete=models.CASCADE,related_name='course_group',null=True,blank=True)
    ClassLink=models.CharField(max_length=500)
    isHeld=models.BooleanField(default=False)
    #isCompleted=models.BooleanField(default=False)#تعیین میکند تمام جلسات کلاس برگزار شده است
    def __str__(self):
        return f'{self.request} - {self.ClassLink}'
    class Meta:
        verbose_name_plural = 'Courses'
        ordering = ['-Time']

class AgreementCourseCreate(models.Model):
    createCourse = models.OneToOneField(CourseCreate, on_delete=models.CASCADE, related_name='createCourse')
    Time = models.DateTimeField()
    ClassLink = models.CharField(max_length=500)#api از وبینار که گرفتیم پر میشود
    isHeld = models.BooleanField(default=False)

    # isCompleted=models.BooleanField(default=False)#تعیین میکند تمام جلسات کلاس برگزار شده است
    def __str__(self):
        return f'{self.request} - {self.ClassLink}'

    class Meta:
        verbose_name_plural = 'Courses'
        ordering = ['-Time']


class WaitingHall(models.Model):
    ClassRequest=models.OneToOneField(CourseRequest, on_delete=models.CASCADE,related_name='waititent',unique=True,null=False,blank=False)
    Title=models.CharField(max_length=200,db_index=True)
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.Title=self.ClassRequest.Title
        self.description=self.ClassRequest.description
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.ClassRequest.Title}is Attention by{self.ClassRequest.Creator}'


class Proposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در حال انتظار '),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده')

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(CourseRequest, on_delete=models.CASCADE)
    message = models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=10,)
    agreement_price=models.BooleanField(default=False)
    status = models.CharField(max_length=300,default='pending',choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Proposals'
        ordering = ['-created_at']


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
    def save(self,*args, **kwargs):
        """اگر این استاد دعوت را بپذیرد، دیگر دعوت‌ها رد شوند و استاد در کلاس ثبت شود."""
        creator=self.course_request.Creator
        if(self.status== 'accepted'):
            self.course_request.accepted_teacher = self.teacher
            self.course_request.save()
            CourseInvitation.objects.filter(course_request=self.course_request).exclude(id=self.id).update(
                status='rejected')
        super().save(*args, **kwargs)
        # تنظیم استاد در کلاس



        # رد کردن سایر دعوت‌ها




class ListCourseRequest(models.Model):
    MyCource=models.ForeignKey(CourseInvitation, on_delete=models.CASCADE,related_name='myclasses')
    def __str__(self):
        return f'{self.MyCource},{self.MyCource.status}'