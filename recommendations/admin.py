from django.contrib import admin
from recommendations.models import RequestLog

# Register your models here.
@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'client_id', 'client_name', 'most_recent_appointment', 
                    'most_recent_purchase', 'reference_code', 'procedures', 
                    'recommended_procedures')