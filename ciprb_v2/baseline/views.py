import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from baseline.models import BaselineAssessment
from baseline.utils import KOBO_MAPPINGS


class KoboIngestView(APIView):
    def post(self, request, *args, **kwargs):
        # Auth check
        secret = request.META.get('HTTP_X_KOBO_WEBHOOK_SECRET')
        expected_secret = os.environ.get('KOBO_WEBHOOK_SECRET', 'test_secret')
        if secret != expected_secret:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data

        # KoboToolbox sends _id as the submission identifier
        # form_type can come from:
        # 1. A calculate field in the form (preferred)
        # 2. The X-Form-Id header Kobo sends
        # 3. The formhub/uuid or _xform_id_string field

        form_type = (
            payload.get('form_type')                    # our calculate field
            or payload.get('_xform_id_string')          # Kobo's form ID string
            or request.META.get('HTTP_X_KOBO_FORM_ID')  # custom header fallback
        )

        # kobo_submission_id: use _id (Kobo's integer ID) or _uuid
        kobo_submission_id = str(
            payload.get('kobo_submission_id')
            or payload.get('_id')
            or payload.get('_uuid')
            or ''
        )

        if not form_type or not kobo_submission_id:
            return Response({
                "error": "Missing form_type or submission ID",
                "received_keys": list(payload.keys())[:20],
                "form_type_found": form_type,
                "submission_id_found": kobo_submission_id,
            }, status=status.HTTP_400_BAD_REQUEST)

        # Normalize form_type: Kobo form_id strings may match exactly
        # Map Kobo _xform_id_string values to our internal names if needed
        form_type_map = {
            'fistula_campaign': 'fistula_campaign',
            'mpdsr_report': 'mpdsr_report',
            'baseline_assessment': 'baseline_assessment',
        }
        form_type = form_type_map.get(form_type, form_type)

        if form_type == 'fistula_campaign':
            model = apps.get_model('tracker', 'FistulaCase')
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)

            mapping = KOBO_MAPPINGS.get('fistula_campaign', {}).get('fields', {})
            data = {}
            for kobo_field, model_field in mapping.items():
                val = payload.get(kobo_field)
                if val is not None:
                    # Convert yes/no booleans from Kobo
                    if model_field in ('has_disability', 'is_ethnic_minority', 'is_displaced'):
                        data[model_field] = str(val).lower() in ('true', 'yes', '1')
                    else:
                        data[model_field] = val

            data['kobo_submission_id'] = kobo_submission_id

            # Defaults for required fields
            data.setdefault('referral_status', 'IDENTIFIED')
            data.setdefault('surgery_outcome', 'PENDING')
            data.setdefault('has_disability', False)
            data.setdefault('is_ethnic_minority', False)
            data.setdefault('is_displaced', False)

            try:
                model.objects.create(**data)
                return Response({"message": "FistulaCase created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e), "data": data}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'mpdsr_report':
            model = apps.get_model('mpdsr', 'MPDSREvent')
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)

            mapping = KOBO_MAPPINGS.get('mpdsr_report', {}).get('fields', {})
            data = {}
            for kobo_field, model_field in mapping.items():
                val = payload.get(kobo_field)
                if val is not None:
                    data[model_field] = val

            data['kobo_submission_id'] = kobo_submission_id
            data.setdefault('action_status', 'PENDING')

            try:
                model.objects.create(**data)
                return Response({"message": "MPDSREvent created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e), "data": data}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'baseline_assessment':
            if BaselineAssessment.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)
            try:
                BaselineAssessment.objects.create(
                    partner=payload.get('partner', 'Unknown'),
                    payload=dict(payload),
                    kobo_submission_id=kobo_submission_id,
                )
                return Response({"message": "BaselineAssessment created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "error": f"Unknown form_type: {form_type}",
            "hint": "form_type must be fistula_campaign, mpdsr_report, or baseline_assessment"
        }, status=status.HTTP_400_BAD_REQUEST)
