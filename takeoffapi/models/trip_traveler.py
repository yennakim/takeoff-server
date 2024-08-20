from django.db import models
from .trip import Trip
from .traveler import Traveler

class TripTraveler(models.Model):
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
  traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
 