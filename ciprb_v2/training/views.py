from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from .models import TrainingSession


def training_log(request):
    sessions = TrainingSession.objects.all().order_by('-session_date')
    total_participants = TrainingSession.objects.aggregate(total=Sum('participants_count'))['total'] or 0
    by_partner = TrainingSession.objects.values('partner').annotate(
        sessions=Count('id'), participants=Sum('participants_count')
    )
    by_competency = TrainingSession.objects.values('competency_level').annotate(count=Count('id'))

    context = {
        'sessions': sessions,
        'total_participants': total_participants,
        'total_sessions': sessions.count(),
        'by_partner': list(by_partner),
        'by_competency': list(by_competency),
    }
    return render(request, 'training/log.html', context)


@require_POST
def add_training(request):
    TrainingSession.objects.create(
        partner=request.POST.get('partner'),
        district=request.POST.get('district'),
        session_date=request.POST.get('session_date'),
        topic=request.POST.get('topic'),
        trainer_name=request.POST.get('trainer_name'),
        participants_count=int(request.POST.get('participants_count', 0)),
        competency_level=request.POST.get('competency_level'),
        notes=request.POST.get('notes', ''),
    )
    return redirect('training_log')
