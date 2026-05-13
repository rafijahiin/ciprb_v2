import json
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent
from activities.models import ActivityLog
from training.models import TrainingSession


def dashboard_main(request):
    # --- Fistula ---
    fistula_goal = 100
    fistula_qs = FistulaCase.objects.all()
    fistula_operated = fistula_qs.filter(referral_status='OPERATED').count()
    fistula_total = fistula_qs.count()
    fistula_progress = (fistula_operated / fistula_goal * 100) if fistula_goal > 0 else 0

    # Fistula pipeline breakdown
    pipeline = {}
    for status, label in FistulaCase.REFERRAL_STATUS_CHOICES:
        pipeline[label] = fistula_qs.filter(referral_status=status).count()

    # --- MPDSR ---
    mpdsr_qs = MPDSREvent.objects.all()
    total_mpdsr = mpdsr_qs.count()
    implemented_mpdsr = mpdsr_qs.filter(action_status='IMPLEMENTED').count()
    pending_mpdsr = mpdsr_qs.filter(action_status='PENDING').count()
    stalled_mpdsr = mpdsr_qs.filter(action_status='STALLED').count()
    action_gap_percent = (implemented_mpdsr / total_mpdsr * 100) if total_mpdsr > 0 else 0

    mpdsr_by_district = mpdsr_qs.values('district').annotate(count=Count('event_id')).order_by('-count')
    heatmap_labels = json.dumps([x['district'] for x in mpdsr_by_district])
    heatmap_data = json.dumps([x['count'] for x in mpdsr_by_district])

    mpdsr_events = mpdsr_qs.order_by('-event_id')[:20]

    # --- Partner breakdown ---
    partners = ['CIPRB', 'PHD', 'Bondhu']
    partner_data = {}
    for p in partners:
        partner_data[p] = {
            'fistula_cases': FistulaCase.objects.count(),  # no partner field on fistula yet
            'activities': ActivityLog.objects.filter(partner=p).count(),
            'beneficiaries': ActivityLog.objects.filter(partner=p).aggregate(t=Sum('beneficiary_count'))['t'] or 0,
            'trainings': TrainingSession.objects.filter(partner=p).count(),
            'participants': TrainingSession.objects.filter(partner=p).aggregate(t=Sum('participants_count'))['t'] or 0,
        }

    partner_labels = json.dumps(partners)
    partner_activities = json.dumps([partner_data[p]['activities'] for p in partners])
    partner_beneficiaries = json.dumps([partner_data[p]['beneficiaries'] for p in partners])

    # --- Progress / flagging ---
    activity_targets = {'CIPRB': 50, 'PHD': 30, 'Bondhu': 20}
    alerts = []
    for p in partners:
        actual = partner_data[p]['activities']
        target = activity_targets.get(p, 30)
        pct = (actual / target * 100) if target > 0 else 0
        if pct < 50:
            alerts.append({'partner': p, 'actual': actual, 'target': target, 'pct': round(pct, 1), 'level': 'critical'})
        elif pct < 80:
            alerts.append({'partner': p, 'actual': actual, 'target': target, 'pct': round(pct, 1), 'level': 'warning'})

    # --- Activities ---
    recent_activities = ActivityLog.objects.order_by('-activity_date', '-created_at')[:10]
    total_beneficiaries = ActivityLog.objects.aggregate(t=Sum('beneficiary_count'))['t'] or 0

    # --- Training ---
    total_participants = TrainingSession.objects.aggregate(t=Sum('participants_count'))['t'] or 0
    total_training_sessions = TrainingSession.objects.count()

    context = {
        # Fistula
        'fistula_operated': fistula_operated,
        'fistula_total': fistula_total,
        'fistula_goal': fistula_goal,
        'fistula_progress': round(fistula_progress, 1),
        'pipeline': pipeline,
        # MPDSR
        'total_mpdsr': total_mpdsr,
        'implemented_mpdsr': implemented_mpdsr,
        'pending_mpdsr': pending_mpdsr,
        'stalled_mpdsr': stalled_mpdsr,
        'action_gap_percent': round(action_gap_percent, 1),
        'heatmap_labels': heatmap_labels,
        'heatmap_data': heatmap_data,
        'mpdsr_events': mpdsr_events,
        # Partners
        'partner_data': partner_data,
        'partner_labels': partner_labels,
        'partner_activities': partner_activities,
        'partner_beneficiaries': partner_beneficiaries,
        # Alerts
        'alerts': alerts,
        # Activities
        'recent_activities': recent_activities,
        'total_beneficiaries': total_beneficiaries,
        # Training
        'total_participants': total_participants,
        'total_training_sessions': total_training_sessions,
    }
    context['fistula_cases'] = FistulaCase.objects.all().order_by('-id')
    context['training_sessions'] = TrainingSession.objects.all().order_by('-session_date')
    return render(request, 'dashboard/main.html', context)
