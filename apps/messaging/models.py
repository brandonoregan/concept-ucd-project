from django.db import models
from apps.users.models import CustomUser

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    unopened = models.BooleanField(default=False)

    # Provides a string representation of an object
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.subject}"