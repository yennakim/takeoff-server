# Generated by Django 4.1.3 on 2024-09-03 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takeoffapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='travelers',
            field=models.ManyToManyField(related_name='trips', through='takeoffapi.TripTraveler', to='takeoffapi.traveler'),
        ),
    ]
