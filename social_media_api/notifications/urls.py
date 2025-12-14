from django.urls import path
from .views import (
    NotificationListView,
    MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView
)

urlpatterns = [
    # List all notifications for authenticated user
    path('', NotificationListView.as_view(), name='notification-list'),
    
    # Mark specific notification as read
    path('<int:pk>/read/', MarkNotificationAsReadView.as_view(), name='notification-mark-read'),
    
    # Mark all notifications as read
    path('read-all/', MarkAllNotificationsAsReadView.as_view(), name='notification-mark-all-read'),
]
