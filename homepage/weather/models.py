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


class Consumption(models.Model):
    date = models.TextField()
    total_km = models.IntegerField()
    traveled_km = models.IntegerField()
    total_fuel = models.IntegerField()
    curent_consuption = models.IntegerField()

    def __str__(self):
        return f'Last consumption was {self.curent_consuption}'

