from django.contrib import admin
from .models import Procedure

# Register your models here.

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost', 
                    'duration', 'expiration', 'reference_code',
                    'region', 'complaint')