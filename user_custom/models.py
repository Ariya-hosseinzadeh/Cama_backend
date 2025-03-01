from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.fields import ChoiceField
from django.core.validators import RegexValidator
import uuid
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
    NationalCode = models.IntegerField(null=True, blank=True)
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