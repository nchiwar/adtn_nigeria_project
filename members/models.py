from django.db import models

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

class Publication(models.Model):
    title = models.CharField(max_length=200)
    brief_description = models.TextField()
    file = models.FileField(upload_to='publications/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title