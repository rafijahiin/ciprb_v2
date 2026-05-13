import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='MPDSREvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('death_type', models.CharField(choices=[('MATERNAL', 'Maternal'), ('PERINATAL', 'Perinatal'), ('STILLBIRTH', 'Stillbirth')], max_length=20)),
                ('age_of_deceased', models.IntegerField()),
                ('district', models.CharField(max_length=255)),
                ('facility_name', models.CharField(max_length=255)),
                ('cause_of_death', models.TextField()),
                ('social_autopsy_findings', models.TextField()),
                ('recommended_action', models.TextField()),
                ('action_status', models.CharField(choices=[('PENDING', 'Pending'), ('FUNDED', 'Funded'), ('IMPLEMENTED', 'Implemented'), ('STALLED', 'Stalled')], max_length=20)),
                ('kobo_submission_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
