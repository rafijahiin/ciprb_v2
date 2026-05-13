import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from baseline.models import BaselineAssessment
from baseline.utils import KOBO_MAPPINGS


class KoboIngestView(APIView):
    def post(self, request, *args, **kwargs):
        secret = request.META.get('HTTP_X_KOBO_WEBHOOK_SECRET')
        expected_secret = os.environ.get('KOBO_WEBHOOK_SECRET', 'test_secret')

        if secret != expected_secret:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data
        form_type = payload.get('form_type')
        kobo_submission_id = payload.get('kobo_submission_id')

        if not form_type or not kobo_submission_id:
            return Response({"error": "Missing form_type or kobo_submission_id"}, status=status.HTTP_400_BAD_REQUEST)

        if form_type == 'fistula_campaign':
            model = apps.get_model('tracker', 'FistulaCase')
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)
            mapping = KOBO_MAPPINGS.get('fistula_campaign', {}).get('fields', {})
            data = {model_field: payload[kobo_field] for kobo_field, model_field in mapping.items() if kobo_field in payload}
            data['kobo_submission_id'] = kobo_submission_id
            try:
                model.objects.create(**data)
                return Response({"message": "FistulaCase created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'mpdsr_report':
            model = apps.get_model('mpdsr', 'MPDSREvent')
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)
            mapping = KOBO_MAPPINGS.get('mpdsr_report', {}).get('fields', {})
            data = {model_field: payload[kobo_field] for kobo_field, model_field in mapping.items() if kobo_field in payload}
            data['kobo_submission_id'] = kobo_submission_id
            try:
                model.objects.create(**data)
                return Response({"message": "MPDSREvent created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'baseline_assessment':
            if BaselineAssessment.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)
            try:
                BaselineAssessment.objects.create(
                    partner=payload.get('partner', 'Unknown'),
                    payload=payload,
                    kobo_submission_id=kobo_submission_id
                )
                return Response({"message": "BaselineAssessment created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": f"Unknown form_type: {form_type}"}, status=status.HTTP_400_BAD_REQUEST)
