from django.shortcuts import render


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_custom.models import CustomUser
from .models import Topic, ResponseTopic, Report
from .Serializers import TopicSerializer, PostSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Topic.objects.filter(is_closed=False)
    def perform_create(self, serializer):
        creator=CustomUser.objects.get(id=1)
        serializer.save(created_by=creator)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()



        # فقط سازنده می‌تواند تاپیک را حذف کند
        if instance.created_by != request.user:
            return Response({"detail": "شما اجازه حذف این تاپیک را ندارید."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        topic = self.get_object()
        posts = topic.posts.order_by('created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def close(self, request, pk=None):
        topic = self.get_object()
        if topic.created_by != request.user:
            return Response({'error': 'اجازه نداری'}, status=403)

        topic.is_closed = True
        topic.save()
        return Response({'message': 'تاپیک بسته شد'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = ResponseTopic.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        creator=CustomUser.objects.get(id=1)
        serializer.save(created_by=creator)

    @action(detail=True, methods=['post'])
    def report(self, request, pk=None):
        post = self.get_object()
        reason = request.data.get('reason', '')
        rust=CustomUser.objects.get(id=1)
        Report.objects.create(
            # user=request.user,
            user=rust,
            post=post,
            reason=reason,
        )
        return Response({'message': 'گزارش ثبت شد'})

# class TopicPostsListView(ListAPIView):
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         topic = Topic.objects.get(slug=slug)
#         return topic.posts.order_by('created_at')  # یا -created_at برای معکوس