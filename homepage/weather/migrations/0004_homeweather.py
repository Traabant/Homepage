# Generated by Django 2.1.7 on 2020-03-30 08:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_consumption_events_gallery_pollution_weather2_weather_forcast'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
            ],
        ),
    ]