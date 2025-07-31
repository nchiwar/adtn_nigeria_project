from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']