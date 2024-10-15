from django.contrib import admin
from recommendations.models import RequestLog

# Register your models here.
@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'client_name', 'most_recent_appointment', 'most_recent_purchase', 'procedures', 'recommended_procedures', 'timestamp')