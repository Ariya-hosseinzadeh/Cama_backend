from FollowSystem.models import Follow, Post, PostMedia, RePost
from rest_framework import serializers


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('id','following')
    def validate(self, data):
        # following = self.context.request.user
        # data['following'] = following
        following = data['following']
        follower = data['follower']

        if following == follower:
            raise serializers.ValidationError({'error_message': 'You cannot follow yourself'})

        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError({'error_message': 'You are already following this user'})

        return data
class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = '__all__'
        read_only_fields = ['id']
# class PostSerializer(serializers.ModelSerializer):
#     media = PostMediaSerializer(many=True, read_only=True)
#     class Meta:
#         model = Post
#         fields = '__all__'
#         read_only_fields = ['author','media']#چون میخواستیم در مدیا ها نیز بصورت داینامیک کنترل کنیم چندتا مدیا بتواند بارگذاری شود از این مدل نمیشد باید از یکی پایینی استفاده کنیم

    # def create(self, validated_data):#در خود ویو آن را کنترل کردیم
    #     author = self.context['request'].user
    #     return Post.objects.create(author=author, **validated_data)

class PostSerializer(serializers.ModelSerializer):
    media_preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author','media']

    def get_media_preview(self, obj):
        medias = obj.media.all()[:3]  # فقط ۳ مدیا اول
        return PostMediaSerializer(medias, many=True).data
class RePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RePost
        fields = '__all__'
        read_only_fields = ['id']
