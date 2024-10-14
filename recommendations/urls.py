# recommendations/urls.py

from django.urls import path
from .views import RecommendationsViewSet

urlpatterns = [
    path('recommend/', RecommendationsViewSet.as_view({'post': 'recommend'})),  # Call 'recommend', not 'recommended'
]