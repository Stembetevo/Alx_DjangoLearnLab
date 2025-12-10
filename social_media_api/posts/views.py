from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from accounts.models import User


# Create your views here.

class FeedView(generics.ListAPIView):
    """
    View for generating a personalized feed for the authenticated user.
    Returns posts from users that the current user follows, ordered by creation date (most recent first).
    GET: Retrieve feed of posts from followed users
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get the current authenticated user
        user = self.request.user
        
        # Get all users that the current user is following
        following_users = user.following.all() #type:ignore
        
        # Get posts from followed users, ordered by created_at (most recent first)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return posts


class PostListCreateView(generics.ListCreateAPIView):
    """
    View for listing all posts and creating new posts.
    GET: List all posts
    POST: Create a new post (authenticated users only)
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific post.
    GET: Retrieve a post
    PUT/PATCH: Update a post (author only)
    DELETE: Delete a post (author only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        # Only the author can update or delete their post
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorPermission()]
        return super().get_permissions()


class CommentListCreateView(generics.ListCreateAPIView):
    """
    View for listing comments on a post and creating new comments.
    GET: List all comments for a specific post
    POST: Create a new comment (authenticated users only)
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Get comments for a specific post
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user and post from URL
        post_id = self.kwargs.get('post_id')
        serializer.save(user=self.request.user, post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific comment.
    GET: Retrieve a comment
    PUT/PATCH: Update a comment (author only)
    DELETE: Delete a comment (author only)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        # Only the comment author can update or delete their comment
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
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
