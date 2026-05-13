from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_log, name='training_log'),
    path('add/', views.add_training, name='add_training'),
]
