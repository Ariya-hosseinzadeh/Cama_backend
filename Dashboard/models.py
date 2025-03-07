from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.aggregates import Avg
from rest_framework.authtoken.admin import User
from django.contrib.contenttypes.models import ContentType

from Rating.models import Rating, Comment
from user_custom.models import CustomUser


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sender_notifications')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment)
    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)
    def update_average_rating(self):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        ratings = Rating.objects.filter(content_type=content_type, object_id=self.id)
        avg = ratings.aggregate(models.Avg('score'))['score__avg']
        self.average_rating = avg if avg else 0
        self.save()