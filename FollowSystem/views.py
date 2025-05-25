from django.shortcuts import render
from rest_framework import viewsets, generics

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny

from .models import Follow
from .serializers import FollowSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # فقط دنبال‌کنندگان یا دنبال‌شونده‌های خود کاربر را نمایش بده
        user = self.request.user
        return Follow.objects.filter(follower=user) | Follow.objects.filter(following=user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
from .models import Post
from .serializers import PostSerializer

class AllPostViewApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # می‌تونی فقط پست‌های کسانی که کاربر دنبال می‌کنه رو فیلتر کنی
        user = self.request.user
        followings = user.following.values_list('following_id', flat=True)
        return Post.objects.filter(author__id__in=followings).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from .models import PostMedia
from .serializers import PostMediaSerializer

class PostMediaViewSet(viewsets.ModelViewSet):
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer
    permission_classes = [permissions.IsAuthenticated]
from .models import RePost
from .serializers import RePostSerializer

class RePostViewSet(viewsets.ModelViewSet):
    queryset = RePost.objects.all()
    serializer_class = RePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

