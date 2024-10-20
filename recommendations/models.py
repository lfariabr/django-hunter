from django.db import models

# Create your models here.
class RequestLog(models.Model):
    client_id = models.CharField(max_length=255, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    most_recent_appointment = models.DateTimeField(null=True, blank=True)
    most_recent_purchase = models.DateTimeField(null=True, blank=True)
    reference_code = models.CharField(max_length=255, null=True, blank=True)
    procedures = models.JSONField()  # Store the procedures list in JSON format
    recommended_procedures = models.JSONField()  # Stores the recommendations sent back
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RequestLog({self.client_id}, {self.client_name})"