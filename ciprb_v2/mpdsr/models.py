import uuid
from django.db import models


class MPDSREvent(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    DEATH_TYPE_CHOICES = [
        ('MATERNAL', 'Maternal'),
        ('PERINATAL', 'Perinatal'),
        ('STILLBIRTH', 'Stillbirth'),
    ]
    death_type = models.CharField(max_length=20, choices=DEATH_TYPE_CHOICES)
    age_of_deceased = models.IntegerField()
    district = models.CharField(max_length=255)
    facility_name = models.CharField(max_length=255)
    cause_of_death = models.TextField()
    social_autopsy_findings = models.TextField()
    recommended_action = models.TextField()

    ACTION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FUNDED', 'Funded'),
        ('IMPLEMENTED', 'Implemented'),
        ('STALLED', 'Stalled'),
    ]
    action_status = models.CharField(max_length=20, choices=ACTION_STATUS_CHOICES)
    kobo_submission_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.event_id} - {self.death_type}"
