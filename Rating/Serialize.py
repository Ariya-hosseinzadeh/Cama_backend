from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from user_custom.models import CustomUser
from .models import Rating,Comment

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score', 'content_type', 'object_id']

    def create(self, validated_data):
        """
        ثبت یا به‌روزرسانی امتیاز کاربر روی یک محتوا
        """
        #user = self.context['request'].user
        user=CustomUser.objects.get(id=1)
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']

        rating, created = Rating.objects.update_or_create(
            user=user, content_type=content_type, object_id=object_id,
            defaults={'score': validated_data['score']}
        )

        # اگر محتوای امتیاز داده شده یک کلاس باشد، میانگین آن را به‌روز کنیم
        if content_type.model == 'courserequest':
            instance = content_type.get_object_for_this_type(id=object_id)

            # بررسی اینکه آیا کاربر جزو دانش‌آموزان این کلاس بوده است
            if user in instance.students.all():
                if instance.is_Hell:
                    instance.update_average_rating()
            else:
                raise serializers.ValidationError("شما در این کلاس حضور نداشته‌اید و نمی‌توانید امتیاز دهید.")
        if content_type.model == 'article':
            instance = content_type.get_object_for_this_type(id=object_id)
            instance.update_average_rating()

        return rating


from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content_type', 'object_id', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        """ ثبت نظر جدید فقط در صورتی که مدل موردنظر معتبر باشد """
        user = self.context['request'].user
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']

        # بررسی اینکه آیا مدل موردنظر اجازه دریافت کامنت دارد
        if content_type.model not in ['course', 'article']:#باید تغغیر کند
            raise serializers.ValidationError("نمی‌توانید برای این نوع محتوا نظر ارسال کنید!")

        return Comment.objects.create(user=user, **validated_data)