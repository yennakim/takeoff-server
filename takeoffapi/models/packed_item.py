from django.db import models
from .trip import Trip


class PackedItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
