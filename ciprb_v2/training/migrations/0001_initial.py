import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='TrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(choices=[('CIPRB', 'CIPRB'), ('PHD', 'PHD'), ('Bondhu', 'Bondhu')], max_length=20)),
                ('district', models.CharField(max_length=255)),
                ('session_date', models.DateField()),
                ('topic', models.CharField(max_length=255)),
                ('trainer_name', models.CharField(max_length=255)),
                ('participants_count', models.IntegerField(default=0)),
                ('competency_level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('DEVELOPING', 'Developing'), ('PROFICIENT', 'Proficient'), ('EXPERT', 'Expert')], default='BEGINNER', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
