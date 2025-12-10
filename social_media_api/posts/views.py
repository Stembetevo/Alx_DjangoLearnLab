from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from accounts.models import User


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for posts and comments.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeedView(generics.ListAPIView):
    """
    View for generating a personalized feed for the authenticated user.
    Returns posts from users that the current user follows, ordered by creation date (most recent first).
    GET: Retrieve feed of posts from followed users
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # Get the current authenticated user
        user = self.request.user
        
        # Get all users that the current user is following
        following_users = user.following.all() #type:ignore
        
        # Get posts from followed users, ordered by created_at (most recent first)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return posts


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on posts.
    
    list: GET /posts/ - List all posts (with pagination and filtering)
    create: POST /posts/ - Create a new post (authenticated users only)
    retrieve: GET /posts/{id}/ - Retrieve a specific post
    update: PUT/PATCH /posts/{id}/ - Update a post (author only)
    destroy: DELETE /posts/{id}/ - Delete a post (author only)
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        # Only the post author can update or delete their post
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorPermission()]
        return super().get_permissions()
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on comments.
    
    list: GET /comments/ - List all comments (with pagination)
    create: POST /comments/ - Create a new comment (authenticated users only)
    retrieve: GET /comments/{id}/ - Retrieve a specific comment
    update: PUT/PATCH /comments/{id}/ - Update a comment (author only)
    destroy: DELETE /comments/{id}/ - Delete a comment (author only)
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        # Only the comment author can update or delete their comment
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCommentAuthorPermission()]
        return super().get_permissions()


# Custom Permission Classes
class IsAuthorPermission(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the post
        return obj.author == request.user


class IsCommentAuthorPermission(permissions.BasePermission):
    """
    Custom permission to only allow authors of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the comment
        return obj.user == request.user
