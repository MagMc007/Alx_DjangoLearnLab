from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """ a model for notifications between users """
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions")
    verb = models.CharField(max_length=255)

    # Generic relation on comment, post or some other model with in the projects
    target_content = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="targeted_content")
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey("target_content", "target_object_id")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    