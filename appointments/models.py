from django.db import models
from django.contrib.auth.models import User
from procedures.models import Procedure

# Create your models here.
class ServedAppointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    employee_name = models.CharField(max_length=100)
    procedure = models.ManyToManyField(Procedure)  # Many-to-many relationship with Procedure
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    store_id = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    store_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Appointment for {self.customer_id} with {self.employee_name} on {self.appointment_date}"