
from classroom.models import *
from django.db import models
from rest_framework.authtoken.admin import User

from user_custom.models import CustomUser


# Create your models here.
class Review(models.Model):
    RatingID = models.AutoField(primary_key=True)
    Commenter=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Commenter')
    Audience=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Audience')
    BehavioralRank=models.DecimalField(decimal_places=2, max_digits=10)
    AcademicRank=models.DecimalField(decimal_places=2, max_digits=10)
    Comments=models.TextField()

class RatingPerson(models.Model):
    RatingPersonID = models.AutoField(primary_key=True)
    UserID=models.ForeignKey(User,on_delete=models.CASCADE)
    BehavioralRank = models.DecimalField(decimal_places=3, max_digits=10,default=0)
    AcademicRank = models.DecimalField(decimal_places=3, max_digits=10,default=0)


class Comment(models.Model):
    CommentID=models.AutoField(primary_key=True)
    Author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Author')
    Audience=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Comment=models.TextField()
    AcceptingCount=models.IntegerField()



