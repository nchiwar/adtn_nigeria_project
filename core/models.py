# core/models.py
from django.db import models

class CpdArticle(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    cpd_hours = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class About(models.Model):
    about_description = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    core_values = models.TextField()
    goals = models.TextField()
    history_summary = models.TextField()
    formation_summary = models.TextField()

    def __str__(self):
        return "About ADTN"

class Official(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='officials/', null=True, blank=True)

    def __str__(self):
        return self.name

class History(models.Model):
    history_content = models.TextField()
    change_designation = models.TextField()
    salary_scale = models.TextField()
    training_institutions = models.TextField()

    def __str__(self):
        return "History of DTN"

class Formation(models.Model):
    formation_content = models.TextField()

    def __str__(self):
        return "Formation of ADTN"