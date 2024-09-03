from django.db import models
from .trip import User, Trip, Traveler


class BoardingPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    departing_from = models.CharField(max_length=50)
    arriving_to = models.CharField(max_length=50)
    airline = models.CharField(max_length=50)
    gate = models.CharField(max_length=50)
    seat = models.CharField(max_length=50)
    departure_time = models.CharField(max_length=50)
    arrival_time = models.CharField(max_length=50)
    flight_number = models.CharField(max_length=50)
    
    
