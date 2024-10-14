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

    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)