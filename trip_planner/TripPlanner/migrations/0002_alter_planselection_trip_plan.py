# Generated by Django 4.2.6 on 2024-03-27 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TripPlanner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planselection',
            name='trip_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TripPlanner.tripplan'),
        ),
    ]
