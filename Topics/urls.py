# yourapp/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TopicViewSet, PostViewSet

router = DefaultRouter()
router.register(r'my-topics', TopicViewSet, basename='topic')
router.register(r'response-topics', PostViewSet, basename='response-topic')

urlpatterns = [
    path('', include(router.urls)),
]
