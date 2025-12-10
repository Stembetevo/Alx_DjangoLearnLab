from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeedView,
    PostViewSet,
    CommentViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Feed endpoint - shows posts from followed users
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Include router URLs for posts and comments viewsets
    path('', include(router.urls)),
]
