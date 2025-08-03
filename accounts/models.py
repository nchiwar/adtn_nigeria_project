from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    membership_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    membership_type = models.CharField(max_length=50, choices=[('Full', 'Full'), ('Associate', 'Associate')], blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email