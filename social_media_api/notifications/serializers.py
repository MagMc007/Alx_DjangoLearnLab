from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """ handle notifications data"""
    actor = serializers.StringRelatedField()
    target = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "target", "timestamp", "is_read"]
