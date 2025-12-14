from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notifications
from .serializers import NotificationSerializer


# Create your views here.

class NotificationPagination(PageNumberPagination):
    """
    Pagination class for notifications.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NotificationListView(generics.ListAPIView):
    """
    View for listing all notifications for the authenticated user.
    GET: Retrieve all notifications, with unread notifications prominently shown.
    Only authenticated users can access their own notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination
    
    def get_queryset(self):
        """
        Return notifications for the authenticated user.
        Unread notifications appear first, followed by read notifications.
        """
        user = self.request.user
        
        # Get all notifications for the user, ordered by read status and timestamp
        # Unread notifications (read=False) come first due to ordering
        return Notifications.objects.filter(recipient=user).order_by('read', '-timestamp')
    
    def list(self, request, *args, **kwargs):
        """
        Override list to include unread count in response.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get count of unread notifications
        unread_count = queryset.filter(read=False).count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['unread_count'] = unread_count
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'unread_count': unread_count
        })


class MarkNotificationAsReadView(APIView):
    """
    View for marking a notification as read.
    POST: Mark a specific notification as read by its ID.
    Only the recipient can mark their notification as read.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = Notifications.objects.get(pk=pk, recipient=request.user)
        except Notifications.DoesNotExist:
            return Response(
                {'error': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Mark as read
        notification.read = True
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response({
            'message': 'Notification marked as read.',
            'notification': serializer.data
        }, status=status.HTTP_200_OK)


class MarkAllNotificationsAsReadView(APIView):
    """
    View for marking all notifications as read.
    POST: Mark all unread notifications as read for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Update all unread notifications to read
        updated_count = Notifications.objects.filter(
            recipient=user,
            read=False
        ).update(read=True)
        
        return Response({
            'message': f'{updated_count} notification(s) marked as read.',
            'count': updated_count
        }, status=status.HTTP_200_OK)
