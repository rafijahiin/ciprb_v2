from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from .models import ActivityLog


def activity_tracker(request):
    logs = ActivityLog.objects.all().order_by('-activity_date', '-created_at')
    total_beneficiaries = ActivityLog.objects.aggregate(total=Sum('beneficiary_count'))['total'] or 0
    by_partner = ActivityLog.objects.values('partner').annotate(
        count=Count('id'), beneficiaries=Sum('beneficiary_count')
    )
    by_type = ActivityLog.objects.values('activity_type').annotate(count=Count('id')).order_by('-count')[:10]

    context = {
        'logs': logs,
        'total_beneficiaries': total_beneficiaries,
        'total_activities': logs.count(),
        'by_partner': list(by_partner),
        'by_type': list(by_type),
    }
    return render(request, 'activities/tracker.html', context)


@require_POST
def add_activity(request):
    ActivityLog.objects.create(
        partner=request.POST.get('partner'),
        district=request.POST.get('district'),
        upazila=request.POST.get('upazila'),
        activity_type=request.POST.get('activity_type'),
        activity_date=request.POST.get('activity_date'),
        staff_name=request.POST.get('staff_name'),
        beneficiary_count=int(request.POST.get('beneficiary_count', 0)),
        notes=request.POST.get('notes', ''),
    )
    return redirect('activity_tracker')
