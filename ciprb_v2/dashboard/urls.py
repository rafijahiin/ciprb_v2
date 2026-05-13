from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_main, name='dashboard_main'),
]
