from django.db import models
from django.utils import timezone

# Create your models here.


class Weather(models.Model):
    date = models.DateTimeField(default=timezone.now)
    weather_today = models.TextField()

    def __str__(self):
        return (self.weather_today)


class Weather2(models.Model):
    date = models.TextField()
    weather_today = models.TextField()

    def __str__(self):
        return self.weather_today
