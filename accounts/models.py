from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
