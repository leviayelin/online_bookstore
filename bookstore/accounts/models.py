from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(default='media/default-user-image.png', blank=True, null=True)

    def __str__(self):
        return self.username
