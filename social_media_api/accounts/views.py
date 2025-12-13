from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from .models import User

# Alias for CustomUser
CustomUser = User

# Create your views here.
class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #type:ignore
        
        # Token is created by the serializer, just retrieve it
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,# type: ignore
                'username': user.username, # type: ignore
                'email': user.email # type: ignore
            } 
        }, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']  #type: ignore
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating the authenticated user's profile.
    GET: Retrieve current user's profile
    PUT/PATCH: Update current user's profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Return the authenticated user's profile
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    """
    View for following another user.
    POST: Follow a user by their user_id
    Only authenticated users can follow others.
    Users cannot follow themselves.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def post(self, request, user_id):
        # Get the user to follow
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Prevent users from following themselves
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are already following {user_to_follow.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following list (user follows user_to_follow)
        request.user.following.add(user_to_follow)
        
        return Response(
            {
                'message': f'You are now following {user_to_follow.username}.',
                'user': {
                    'id': user_to_follow.id, #type: ignore
                    'username': user_to_follow.username
                }
            },
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def post(self, request, user_id):
        # Get the user to unfollow
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # Check if currently following
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'error': f'You are not following {user_to_unfollow.username}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove from following list
        request.user.following.remove(user_to_unfollow)
        
        return Response(
            {
                'message': f'You have unfollowed {user_to_unfollow.username}.',
                'user': {
                    'id': user_to_unfollow.id,  # type: ignore
                    'username': user_to_unfollow.username
                }
            },
            status=status.HTTP_200_OK
        )
