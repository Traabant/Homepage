from django.db import models
from django.utils import timezone

class Weather(models.Model):
    date = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField()
    pressure = models.FloatField()

    def __str__(self):
        return (self.temperature)
