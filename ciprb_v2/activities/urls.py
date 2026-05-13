from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_tracker, name='activity_tracker'),
    path('add/', views.add_activity, name='add_activity'),
]
