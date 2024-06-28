from django.db import models
import uuid

# Create your models here.

class License(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    domain = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    def __str__(self):
        return str(self.domain) + f" {self.key}"
