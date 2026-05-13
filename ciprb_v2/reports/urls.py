from django.urls import path
from . import views

urlpatterns = [
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/ppt/', views.export_ppt, name='export_ppt'),
    path('generate-newsletter/', views.generate_newsletter, name='generate_newsletter'),
]
