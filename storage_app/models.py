from django.db import models
from django.contrib.auth.models import User
import os
import uuid

def user_directory_path(instance, filename):
    return f'user_{instance.owner.id}/{uuid.uuid4()}_{filename}'

class File(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'Can View'),
        ('edit', 'Can Edit'),
        ('none', 'No Access'),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_files')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.name)
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.get_file_type()
        super().save(*args, **kwargs)

    def get_file_type(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        file_types = {
            '.pdf': 'PDF',
            '.doc': 'Word',
            '.docx': 'Word',
            '.txt': 'Text',
            '.jpg': 'Image',
            '.jpeg': 'Image',
            '.png': 'Image',
            '.gif': 'Image',
            '.mp4': 'Video',
            '.avi': 'Video',
            '.mov': 'Video',
            '.mp3': 'Audio',
            '.wav': 'Audio',
            '.zip': 'Archive',
            '.rar': 'Archive',
        }
        return file_types.get(ext, 'Unknown')

    def __str__(self):
        return self.name

class FileShare(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'Can View'),
        ('edit', 'Can Edit'),
    ]

    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='view')
    shared_at = models.DateTimeField(auto_now_add=True)
    can_download = models.BooleanField(default=True)

    class Meta:
        unique_together = ['file', 'user']

    def __str__(self):
        return f"{self.file.name} shared with {self.user.username}"