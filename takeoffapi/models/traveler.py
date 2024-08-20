from django.db import models

class Traveler(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  image = models.CharField(max_length=100)
