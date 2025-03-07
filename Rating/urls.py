from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Rating.views import RatingView, CommentViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
urlpatterns = [
path('ratings-create/', RatingView.as_view(), name='rating-create'),
path('', include(router.urls)),
]