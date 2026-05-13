from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(choices=[('CIPRB', 'CIPRB'), ('PHD', 'PHD'), ('Bondhu', 'Bondhu')], max_length=20)),
                ('district', models.CharField(max_length=255)),
                ('upazila', models.CharField(max_length=255)),
                ('activity_type', models.CharField(max_length=255)),
                ('activity_date', models.DateField(blank=True, null=True)),
                ('staff_name', models.CharField(max_length=255)),
                ('beneficiary_count', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
