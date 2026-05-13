from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import MPDSREvent


@require_POST
@csrf_exempt
def update_action_status(request, event_id):
    event = get_object_or_404(MPDSREvent, event_id=event_id)
    new_status = request.POST.get('action_status')

    if not new_status and request.POST:
        new_status = list(request.POST.values())[0]

    if new_status in dict(MPDSREvent.ACTION_STATUS_CHOICES):
        event.action_status = new_status
        event.save()

    return render(request, 'dashboard/partials/status_dropdown.html', {'event': event})
