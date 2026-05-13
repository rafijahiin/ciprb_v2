from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('', include('baseline.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('mpdsr/', include('mpdsr.urls')),
    path('reports/', include('reports.urls')),
    path('activities/', include('activities.urls')),
    path('training/', include('training.urls')),
]
