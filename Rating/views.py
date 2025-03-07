from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .Serialize import *

class RatingView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = RatingSerializer
    def post(self, request):
        serializer = RatingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "امتیاز شما ثبت شد."}, status=201)
        return Response(serializer.errors, status=400)

from rest_framework import viewsets

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """ هنگام ایجاد، کامنت را به کاربر فعلی نسبت می‌دهد """
        serializer.save(user=self.request.user)
