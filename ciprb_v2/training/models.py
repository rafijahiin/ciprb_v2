from django.db import models


class TrainingSession(models.Model):
    PARTNER_CHOICES = [
        ('CIPRB', 'CIPRB'),
        ('PHD', 'PHD'),
        ('Bondhu', 'Bondhu'),
    ]
    COMPETENCY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('DEVELOPING', 'Developing'),
        ('PROFICIENT', 'Proficient'),
        ('EXPERT', 'Expert'),
    ]
    partner = models.CharField(max_length=20, choices=PARTNER_CHOICES)
    district = models.CharField(max_length=255)
    session_date = models.DateField()
    topic = models.CharField(max_length=255)
    trainer_name = models.CharField(max_length=255)
    participants_count = models.IntegerField(default=0)
    competency_level = models.CharField(max_length=20, choices=COMPETENCY_CHOICES, default='BEGINNER')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.partner} - {self.session_date}"
