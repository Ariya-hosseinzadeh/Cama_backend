from django.shortcuts import render
from rest_framework import viewsets

from Tags.models import Category
from Tags.serializers import CategorySerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent=None)  # فقط دسته‌بندی‌های سطح اول
    serializer_class = CategorySerializer