from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Procedure
from .serializers import ProcedureSerializer
from recommendations.algorithm import prepare_data_and_similarity, get_recommendations_multi

# Create your views here.
    
class ProcedureViewSet(viewsets.ReadOnlyModelViewSet):  #ModelViewSet if edit via API
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated for these actions