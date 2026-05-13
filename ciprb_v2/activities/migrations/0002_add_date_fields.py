from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('activities', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='activity_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='beneficiary_count',
            field=models.IntegerField(default=0),
        ),
    ]
