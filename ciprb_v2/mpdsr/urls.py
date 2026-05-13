from django.urls import path
from . import views

urlpatterns = [
    path('update-status/<uuid:event_id>/', views.update_action_status, name='update_action_status'),
]
