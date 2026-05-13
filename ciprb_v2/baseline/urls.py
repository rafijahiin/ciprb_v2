from django.urls import path
from .views import KoboIngestView

urlpatterns = [
    path('api/kobo/ingest/', KoboIngestView.as_view(), name='kobo-ingest'),
]
