from django.db import models
from django.contrib.auth.models import User


class VaultItem(models.Model):
    CATEGORY_CHOICES = [
        ('photo', 'Photo'),
        ('document', 'Document'),
        ('note', 'Note'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='vault_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title