from django.db import models
from django.conf import settings

class FileRecord(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    minio_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with', blank=True)
    