from django.db import models
from django.utils import timezone


# Create your models here.

class repos(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    git_id = models.IntegerField()
    node_id = models.TextField()
    owner_id = models.IntegerField(default=None)
    name = models.TextField()    
    full_name = models.TextField()
    html = models.URLField()
    description = models.TextField()     
    git_html =  models.URLField()

    def __str__(self):
        return self.name

class authors(models.Model):
    git_id = models.IntegerField()
    node_id = models.TextField()
    login = models.TextField()

    def __str__(self):
        return self.login


