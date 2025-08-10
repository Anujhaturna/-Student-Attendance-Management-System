from django.db import models

# Create your models here.
from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=255)  # Title of the announcement
    message = models.TextField()  # The announcement message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.title
