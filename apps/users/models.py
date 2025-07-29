from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
# Create your models here.
from auditlog.registry import auditlog


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    firebase_uid = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        help_text="Firebase User ID, if applicable."
    )

    avatar_url = models.URLField(
        max_length=2000,
        null=True,
        blank=True,
        help_text="URL to the user's avatar image."
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email or self.username
    

auditlog.register(CustomUser)
auditlog.register(Group)