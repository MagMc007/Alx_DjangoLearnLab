from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and updating notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by("-timestamp")

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Custom action to mark all notifications as read"""
        request.user.notifications.update(is_read=True)
        return Response({"detail": "All notifications marked as read"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        """Custom action to mark a single notification as read"""
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)

