from django.db import models

class User(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  image = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  uid = models.CharField(max_length=50)
