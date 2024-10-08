from django.db import models
from .user import User
from .traveler import Traveler

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_name = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    travelers = models.ManyToManyField(Traveler, through= "TripTraveler", related_name="trips")
