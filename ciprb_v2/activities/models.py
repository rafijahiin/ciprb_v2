from django.db import models


class ActivityLog(models.Model):
    PARTNER_CHOICES = [
        ('CIPRB', 'CIPRB'),
        ('PHD', 'PHD'),
        ('Bondhu', 'Bondhu'),
    ]
    partner = models.CharField(max_length=20, choices=PARTNER_CHOICES)
    district = models.CharField(max_length=255)
    upazila = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)
    activity_date = models.DateField(null=True, blank=True)
    staff_name = models.CharField(max_length=255)
    beneficiary_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.activity_type} by {self.partner}"
