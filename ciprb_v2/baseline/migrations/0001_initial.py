import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='BaselineAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('partner', models.CharField(max_length=255)),
                ('payload', models.JSONField()),
                ('kobo_submission_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
