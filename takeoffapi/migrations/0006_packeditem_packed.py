# Generated by Django 4.1.3 on 2024-09-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takeoffapi', '0005_alter_boardingpass_traveler_alter_boardingpass_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='packeditem',
            name='packed',
            field=models.BooleanField(default=False),
        ),
    ]
