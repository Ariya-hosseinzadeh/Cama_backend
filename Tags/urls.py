from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', views.CategoryViewSet)
urlpatterns = [
    path('category/',include(router.urls)),
]