from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['partner', 'district', 'activity_type', 'activity_date', 'beneficiary_count']
    list_filter = ['partner', 'activity_type']
