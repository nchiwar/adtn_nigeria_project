from django.db import models
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class MembershipApplication(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    password = models.CharField(max_length=100)
    dental_qualification = models.CharField(max_length=100)
    membership_type = models.CharField(max_length=50)
    years_of_experience = models.CharField(max_length=10)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.membership_type}"

def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10MB
    if value and hasattr(value, 'size'):  # Check if size attribute exists
        if value.size > max_size:
            raise ValidationError(f'File size must not exceed {max_size / (1024 * 1024)}MB.')

class Publication(models.Model):
    title = models.CharField(max_length=200)
    brief_description = models.TextField()
    file = models.FileField(upload_to='publications/', validators=[validate_file_size])
    cover_image = models.ImageField(upload_to='publication_covers/', default='static/images/placeholder.jpg')  # Default placeholder
    uploaded_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    membership_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    message = models.TextField()
    consent = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
class FAQCategory(models.TextChoices):
    MEMBERSHIP = 'membership', 'Membership'
    ECPD = 'ecpd', 'ECPD'
    REGULATION = 'regulation', 'Regulation'
    PAYMENT = 'payment', 'Payment'

class FAQ(models.Model):
    category = models.CharField(max_length=20, choices=FAQCategory.choices, default=FAQCategory.MEMBERSHIP)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()  # Example field
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Member(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    from django.db import models


