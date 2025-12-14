from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 'object_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 'object_id', 'timestamp']
    
    def get_target_type(self, obj):
        """Get the type of the target object (e.g., 'post', 'comment')"""
        if obj.content_type:
            return obj.content_type.model
        return None
