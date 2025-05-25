from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from user_custom.models import CustomUser

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # کاربری که امتیاز داده است
    score = models.PositiveIntegerField()  # مقدار امتیاز (مثلاً ۱ تا ۵)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # نوع محتوایی که امتیاز گرفته
    object_id = models.PositiveIntegerField()  # شناسه‌ی آن محتوا
    content_object = GenericForeignKey('content_type', 'object_id')  # ارتباط عمومی با مدل‌های مختلف

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')  # هر کاربر فقط یک‌بار روی هر محتوا امتیاز دهد

    def __str__(self):
        return f"{self.user.username} rated {self.score} on {self.content_type.model}"




class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # کاربری که نظر داده است
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # نوع مدلی که کامنت روی آن است
    object_id = models.PositiveIntegerField()  # ID شیء موردنظر (کلاس، مقاله و...)
    content_object = GenericForeignKey('content_type', 'object_id')  # ارتباط عمومی
    text = models.TextField()  # متن نظر
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    def __str__(self):
        return f"Comment by {self.user} on {self.content_type} - {self.object_id}"





# from classroom.models import *
# from django.db import models
# from rest_framework.authtoken.admin import User
#
# from user_custom.models import CustomUser
#
#
# # Create your models here.
# class Review(models.Model):
#     RatingID = models.AutoField(primary_key=True)
#     Commenter=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Commenter')
#     Audience=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Audience')
#     BehavioralRank=models.DecimalField(decimal_places=2, max_digits=10)
#     AcademicRank=models.DecimalField(decimal_places=2, max_digits=10)
#     Comments=models.TextField()
#
# class RatingPerson(models.Model):
#     RatingPersonID = models.AutoField(primary_key=True)
#     UserID=models.ForeignKey(User,on_delete=models.CASCADE)
#     BehavioralRank = models.DecimalField(decimal_places=3, max_digits=10,default=0)
#     AcademicRank = models.DecimalField(decimal_places=3, max_digits=10,default=0)
#
#
# class Comment(models.Model):
#     CommentID=models.AutoField(primary_key=True)
#     Author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Author')
#     Audience=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     Comment=models.TextField()
#     AcceptingCount=models.IntegerField()



