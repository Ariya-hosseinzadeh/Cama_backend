from rest_framework import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FollowViewSet, PostViewSet, PostMediaViewSet, RePostViewSet,AllPostViewApiView

router = DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'post-media', PostMediaViewSet, basename='postmedia')
router.register(r'reposts', RePostViewSet, basename='repost')

urlpatterns = [
    path('', include(router.urls)),
    path('all-post/',AllPostViewApiView.as_view(), name='all-post'),
]
