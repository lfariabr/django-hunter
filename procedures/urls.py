from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcedureViewSet
from recommendations.views import RecommendationsViewSet
from appointments.views import ServedAppointmentsViewSet

router = DefaultRouter()
router.register(r'procedures', ProcedureViewSet)
#router.register(r'appointments', ServedAppointmentsViewSet)
router.register(r'recommended', ServedAppointmentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
