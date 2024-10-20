from django.shortcuts import render
from .models import ServedAppointments
from .serializers import ServedAppointmentsSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ServedAppointmentsViewSet(viewsets.ModelViewSet):
    queryset = ServedAppointments.objects.all()
    serializer_class = ServedAppointmentsSerializer
    permission_classes = [IsAuthenticated]