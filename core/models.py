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