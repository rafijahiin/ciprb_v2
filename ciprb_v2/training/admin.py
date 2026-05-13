from django.contrib import admin
from .models import TrainingSession

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['partner', 'district', 'session_date', 'topic', 'participants_count', 'competency_level']
    list_filter = ['partner', 'competency_level']
