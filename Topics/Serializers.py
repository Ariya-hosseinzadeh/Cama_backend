# serializers.py

from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import timezone

from .models import Topic, ResponseTopic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'content', 'created_by', 'created_at','slug','tags','is_closed']
        read_only_fields = ['created_by', 'created_at','id','slug']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'POST':
            fields.pop('is_closed', None)
        return fields
    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        # فقط نویسنده تاپیک می‌تواند ویرایش کند
        if instance.created_by != user:
            raise serializers.ValidationError("شما اجازه ویرایش این تاپیک را ندارید.")

        # اگر تاپیک پاسخ دارد، ویرایش ممنوع
        if instance.posts.exists():
            raise serializers.ValidationError("تاپیک دارای پاسخ قابل ویرایش نیست.")
        if timezone.now() - instance.created_at > timedelta(minutes=15):
            raise serializers.ValidationError("ویرایش فقط تا ۱۵ دقیقه پس از ایجاد ممکن است.")
        return super().update(instance, validated_data)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseTopic
        fields='__all__'
        read_only_fields = ['created_by', 'created_at',]