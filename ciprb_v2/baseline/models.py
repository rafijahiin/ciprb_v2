import uuid
from django.db import models


class BaselineAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner = models.CharField(max_length=255)
    payload = models.JSONField()
    kobo_submission_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Assessment {self.id} - {self.partner}"
