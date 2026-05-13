import uuid
from django.db import models


class FistulaCase(models.Model):
    patient_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    age = models.IntegerField()
    district = models.CharField(max_length=255)
    upazila = models.CharField(max_length=255)

    REFERRAL_STATUS_CHOICES = [
        ('IDENTIFIED', 'Identified'),
        ('REFERRED', 'Referred'),
        ('ADMITTED', 'Admitted'),
        ('OPERATED', 'Operated'),
        ('REHABILITATED', 'Rehabilitated'),
    ]
    referral_status = models.CharField(max_length=20, choices=REFERRAL_STATUS_CHOICES)

    SURGERY_OUTCOME_CHOICES = [
        ('SUCCESSFUL', 'Successful'),
        ('COMPLICATIONS', 'Complications'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]
    surgery_outcome = models.CharField(max_length=20, choices=SURGERY_OUTCOME_CHOICES)

    has_disability = models.BooleanField(default=False)
    is_ethnic_minority = models.BooleanField(default=False)
    is_displaced = models.BooleanField(default=False)
    kobo_submission_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.patient_id} - {self.district}"
