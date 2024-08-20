from django.db import models
from .trip import Trip

class Lodging(models.Model):
  trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  length_of_stay = models.IntegerField()
