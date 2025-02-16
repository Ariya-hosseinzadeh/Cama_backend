from django.db import models
from rest_framework.authtoken.admin import User

from Tags.models import Tag, Category
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class CourseRequest(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='requester',null=False)
    Title=models.CharField(max_length=200,db_index=True)
    Calling=models.ForeignKey(User, on_delete=models.CASCADE,related_name='calling',null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses",db_index=True)
    tags = models.ManyToManyField(Tag, related_name="courses", blank=True)
    Description=models.TextField()
    CountClass=models.IntegerField(default=1)
    SuggestedTime=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    accepted_teacher=models.ForeignKey(User, on_delete=models.CASCADE,related_name='accepted_teacher',null=True,blank=True)
    def __str__(self):
        return f'{self.Creator} - {self.Title}'
    class Meta:
        verbose_name_plural = 'Class Requests'
        ordering = ['-SuggestedTime']

class Course(models.Model):
    request = models.OneToOneField(CourseRequest, on_delete=models.CASCADE, related_name='class_detail')
    lastCreateTime=models.DateTimeField()
    ClassLink=models.CharField(max_length=500)
    def __str__(self):
        return f'{self.request} - {self.ClassLink}'
    class Meta:
        verbose_name_plural = 'Courses'
        ordering = ['-lastCreateTime']


class WaitingHall(models.Model):
    ClassRequest=models.OneToOneField(CourseRequest, on_delete=models.CASCADE,related_name='waititent')
    is_active=models.BooleanField(default=True)
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
    status = models.CharField(max_length=300,default='pending',choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class CourseInvitation(models.Model):
    course_request = models.ForeignKey(CourseRequest, on_delete=models.CASCADE, related_name="invitations")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations")
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        """اگر این استاد دعوت را بپذیرد، دیگر دعوت‌ها رد شوند و استاد در کلاس ثبت شود."""
        self.status = 'accepted'
        self.save()

        # تنظیم استاد در کلاس
        self.course_request.accepted_teacher = self.teacher
        self.course_request.save()

        # رد کردن سایر دعوت‌ها
        CourseInvitation.objects.filter(course_request=self.course_request).exclude(id=self.id).update(
            status='rejected')
class AttentionUser(models.Model):
    user = models.ManyToManyField(User, related_name='attendant',blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class ListCourseRequest(models.Model):
    MyCource=models.ForeignKey(CourseInvitation, on_delete=models.CASCADE,related_name='myclasses')
    def __str__(self):
        return f'{self.MyCource},{self.MyCource.status}'