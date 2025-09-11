from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    membership_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    membership_type = models.CharField(max_length=50, blank=True, null=True)
    joined_date = models.DateField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    email = models.EmailField(unique=True, max_length=254)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"

class Official(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='officials/', blank=True, null=True)

    def __str__(self):
        return self.name