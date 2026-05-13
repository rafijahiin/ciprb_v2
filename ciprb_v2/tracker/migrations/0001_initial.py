import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='FistulaCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('age', models.IntegerField()),
                ('district', models.CharField(max_length=255)),
                ('upazila', models.CharField(max_length=255)),
                ('referral_status', models.CharField(choices=[('IDENTIFIED', 'Identified'), ('REFERRED', 'Referred'), ('ADMITTED', 'Admitted'), ('OPERATED', 'Operated'), ('REHABILITATED', 'Rehabilitated')], max_length=20)),
                ('surgery_outcome', models.CharField(choices=[('SUCCESSFUL', 'Successful'), ('COMPLICATIONS', 'Complications'), ('FAILED', 'Failed'), ('PENDING', 'Pending')], max_length=20)),
                ('has_disability', models.BooleanField(default=False)),
                ('is_ethnic_minority', models.BooleanField(default=False)),
                ('is_displaced', models.BooleanField(default=False)),
                ('kobo_submission_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
