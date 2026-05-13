from django.db import models
from django.utils import timezone


class MonthlyNewsletter(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Newsletter {self.month}/{self.year}"
