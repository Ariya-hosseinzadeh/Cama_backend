from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from complaint_ticket.models import Complaint
from complaint_ticket.serializers import ComplaintSerializer


# Create your views here.
class ComplaintsList(generics.ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    pagination_class = None
class Coplaint(APIView):
    serializer_class = ComplaintSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    def get(self, request,id):
        data = Complaint.objects.get(id=id)
        serializer = ComplaintSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request,id):
        data = Complaint.objects.get(id=id)
        serializer = ComplaintSerializer(data, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request,id):
        data = Complaint.objects.get(id=id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class createComplaint(APIView):
    serializer_class = ComplaintSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = ComplaintSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



