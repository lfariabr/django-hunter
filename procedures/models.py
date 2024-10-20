from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Procedure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.FloatField()
    duration = models.PositiveIntegerField() # In minutes
    expiration = models.PositiveIntegerField() # In days
    region = models.CharField(max_length=100)
    complaint = models.TextField()
    reference_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name