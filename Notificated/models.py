from django.db import models

from user_custom.models import CustomUser


# Create your models here.
#این کلاس درحالی اضافه شد که وظیفه ارتباط اعلان ها بین کاربران از قبل توسط یک کلاس نوتیف دیگر در داشبر ایجاد سده بود اما برای بهتر کار کردن سیستم کلاسی برای نوتیف های یک طرفه سیستمی ساخته شد
class Notification(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # گیرنده نوتیف
    message = models.TextField()
    # url = models.CharField(max_length=255, blank=True)  # لینک مقصد
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Notifications'
        verbose_name = 'Notification'
    def __str__(self):
        return self.title