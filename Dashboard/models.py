from django.db import models
from rest_framework.authtoken.admin import User

from user_custom.models import CustomUser


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sender_notifications')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title