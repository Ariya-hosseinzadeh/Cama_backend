from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.fields import ChoiceField
from django.core.validators import RegexValidator

import uuid

from cama.upload_paths import profile_image_path

# Create your models here.
password_validator = RegexValidator(
    regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    message="رمز عبور باید حداقل ۸ کاراکتر، شامل حروف بزرگ، حروف کوچک، عدد و کاراکتر خاص باشد."
)
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user_log', 'User'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),

    ]
    codeUser=models.CharField(max_length=12,unique=True,default=str(uuid.uuid4())[:12],blank=False,null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user_log')
    email = models.EmailField(max_length=254, blank=False,unique=True)
    password = models.CharField(max_length=128, validators=[password_validator])
    SoftDeleting = models.BooleanField(default=False,blank=False,null=False)
    is_verified = models.BooleanField(default=False,blank=False,null=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="instructors/", blank=True, null=True)
    average_rating = models.FloatField(default=0)  # ذخیره امتیاز

    def is_employee(self):
        return self.role == 'employee'
    def is_admin(self):
        return self.role == 'admin'
    def is_user(self):
        return self.role == 'user'
class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
# اطلاعات اضافی برای CustomUser
from PIL import Image

class AdditionalInformationUser(models.Model):
    DEGREE_CHOICES = [
        ('diploma', 'دیپلم'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد '),
        ('ph.d', 'دکتری')
    ]


    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='additional_info')
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=profile_image_path,null=True, blank=True)
    gender=models.CharField(max_length=10,choices=[('male','مرد '),('female','زن'),],null=True,blank=True)
    birth_date=models.DateField(blank=True,null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address_line = models.TextField(blank=True)
    job_now = models.ForeignKey('Job',on_delete=models.SET_NULL, null=True, blank=True)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, default='diploma', blank=False)
    skills = models.ManyToManyField('Skills', through='UserSkill', related_name='user_skill')
    CareerHistory=models.ManyToManyField('Job',through='CareerHistory', related_name='career_history')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img_path = self.profile_image.path
            img = Image.open(img_path)
            img = img.convert("RGB")  # اگر فرمت PNG باشد، به RGB تبدیل شود
            img.save(img_path, format="JPEG", quality=70, optimize=True)  # فشرده‌سازی

    def __str__(self):
        return self.user.username


class UserSkill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey('AdditionalInformationUser', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skills', on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    class Meta:
        unique_together = ('user', 'skill')


    def __str__(self):
        return f"{self.user.user.username} - {self.skill.name} ({self.level})"
class Job(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class CareerHistory(models.Model):
    user_data = models.ForeignKey('AdditionalInformationUser', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    company=models.CharField(max_length=100,blank=False,null=False)
    date_start=models.DateField(blank=True,null=True)
    date_end=models.DateField(blank=True,null=True)
    NowBusy=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_data.user.username} - {self.job.name} ({self.company.title})"


# مدل Employee
class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_info')
    HireDate = models.DateField()
    TerminationDate = models.DateField(blank=True, null=True)
    Status = models.BooleanField(default=True)



class Permission(models.Model):
    pass