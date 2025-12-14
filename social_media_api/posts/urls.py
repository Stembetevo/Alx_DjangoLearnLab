from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeedView,
    PostViewSet,
    CommentViewSet,
    LikePostView,
    UnlikePostView
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Feed endpoint - shows posts from followed users
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Like/Unlike endpoints
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    
    # Include router URLs for posts and comments viewsets
    path('', include(router.urls)),
]
