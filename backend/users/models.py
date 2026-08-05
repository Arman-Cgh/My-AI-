from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username