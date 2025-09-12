from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = extra_fields.pop('username', None)
        if username:
            if not username:
                raise ValueError('The Username field must be set')
        else:
            username = email.split('@')[0]
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
    membership_type = models.CharField(
        max_length=50,
        choices=[
            ('full', 'FULL MEMBERSHIP'),
            ('associate', 'ASSOCIATE MEMBERSHIP'),
            ('student', 'STUDENT MEMBERSHIP'),
            ('fellow', 'COLLEGE OF FELLOWS')
        ],
        default='full'
    )
    joined_date = models.DateField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    email = models.EmailField(unique=True, max_length=254)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.email})"

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)  # Keep for compatibility
    status = models.CharField(max_length=20, default='inactive')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    membership_type = models.CharField(
        max_length=50,
        choices=[
            ('full', 'FULL MEMBERSHIP'),
            ('associate', 'ASSOCIATE MEMBERSHIP'),
            ('student', 'STUDENT MEMBERSHIP'),
            ('fellow', 'COLLEGE OF FELLOWS')
        ],
        default='full'
    )

    def __str__(self):
        return f"{self.user.username}'s Subscription ({self.get_membership_type_display()})"

class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50, choices=[
        ('magazine', 'Magazine'),
        ('article', 'Article'),
        ('event', 'Event')
    ])
    item_name = models.CharField(max_length=255)
    paystack_reference = models.CharField(max_length=255, blank=True, null=True)  # Replace stripe_charge_id
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')

    def __str__(self):
        return f"{self.user.username} - {self.item_name}"

class Official(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='officials/', blank=True, null=True)

    def __str__(self):
        return self.name