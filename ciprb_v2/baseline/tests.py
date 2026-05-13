from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from baseline.models import BaselineAssessment
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent
import os


class KoboIngestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('kobo-ingest')
        self.secret = 'test_secret'
        os.environ['KOBO_WEBHOOK_SECRET'] = self.secret

    def test_unauthorized(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fistula_campaign(self):
        payload = {
            'form_type': 'fistula_campaign', 'kobo_submission_id': 'fistula123',
            'age': 30, 'district': 'Dhaka', 'upazila': 'Gulshan',
            'referral_status': 'IDENTIFIED', 'surgery_outcome': 'PENDING',
            'has_disability': False, 'is_ethnic_minority': False, 'is_displaced': False
        }
        response = self.client.post(self.url, payload, format='json', HTTP_X_KOBO_WEBHOOK_SECRET=self.secret)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FistulaCase.objects.filter(kobo_submission_id='fistula123').exists())

    def test_mpdsr_report(self):
        payload = {
            'form_type': 'mpdsr_report', 'kobo_submission_id': 'mpdsr123',
            'death_type': 'MATERNAL', 'age_of_deceased': 25, 'district': 'Sylhet',
            'facility_name': 'Sylhet MAG Osmani', 'cause_of_death': 'Hemorrhage',
            'social_autopsy_findings': 'Delay', 'recommended_action': 'Awareness',
            'action_status': 'PENDING'
        }
        response = self.client.post(self.url, payload, format='json', HTTP_X_KOBO_WEBHOOK_SECRET=self.secret)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_baseline_assessment(self):
        payload = {'form_type': 'baseline_assessment', 'kobo_submission_id': 'baseline123', 'partner': 'CIPRB', 'some_data': 'value'}
        response = self.client.post(self.url, payload, format='json', HTTP_X_KOBO_WEBHOOK_SECRET=self.secret)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_submission(self):
        payload = {
            'form_type': 'fistula_campaign', 'kobo_submission_id': 'fistula123',
            'age': 30, 'district': 'Dhaka', 'upazila': 'Gulshan',
            'referral_status': 'IDENTIFIED', 'surgery_outcome': 'PENDING',
            'has_disability': False, 'is_ethnic_minority': False, 'is_displaced': False
        }
        self.client.post(self.url, payload, format='json', HTTP_X_KOBO_WEBHOOK_SECRET=self.secret)
        response = self.client.post(self.url, payload, format='json', HTTP_X_KOBO_WEBHOOK_SECRET=self.secret)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FistulaCase.objects.filter(kobo_submission_id='fistula123').count(), 1)
