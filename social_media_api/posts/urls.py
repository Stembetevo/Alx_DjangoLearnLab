from django.urls import path
from .views import (
    FeedView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView
)

urlpatterns = [
    # Feed endpoint - shows posts from followed users
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Post endpoints
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # Comment endpoints
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
