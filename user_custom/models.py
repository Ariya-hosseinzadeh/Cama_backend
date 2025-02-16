from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.fields import ChoiceField


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('user_log', 'User'),

    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(max_length=254, blank=False,unique=True)
    NationalCode = models.CharField(max_length=10, blank=False,unique=True,null=False)
    SoftDeleting = models.BooleanField(default=False,blank=False,null=False)
    is_verified = models.BooleanField(default=False,blank=False,null=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="instructors/", blank=True, null=True)
    def is_employee(self):
        return self.role == 'employee'
    def is_admin(self):
        return self.role == 'admin'
    def is_user(self):
        return self.role == 'user'
class Skills(models.Model):
   title=models.CharField(max_length=50)
   Mastery=models.CharField(max_length=50,choices=[('Beginner','beginner'),('Intermediate','intermediate'),('Proficient','proficient'),('Advanced','advanced'),('Expert','expert')],blank=False,)

# اطلاعات اضافی برای CustomUser
class AdditionalInformationUser(models.Model):
    DEGREE_CHOICES = [
        ('diploma', 'دیپلم'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد '),
        ('ph.d', 'دکتری')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='additional_info')
    job = models.CharField(max_length=50, blank=True)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, default='diploma', blank=False)
    skills=models.ForeignKey(Skills, on_delete=models.CASCADE)


# مدل Employee
class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_info')
    HireDate = models.DateField()
    TerminationDate = models.DateField(blank=True, null=True)
    Status = models.BooleanField(default=True)


class Permission(models.Model):
    pass