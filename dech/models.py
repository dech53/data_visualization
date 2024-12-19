# dech/models.py
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    person = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
