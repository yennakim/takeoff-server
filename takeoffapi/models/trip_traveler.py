from django.db import models
from .trip import Trip
from .traveler import Traveler

class TripTraveler(models.Model):
  trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
  traveler_id = models.ForeignKey(Traveler, on_delete=models.CASCADE)
 