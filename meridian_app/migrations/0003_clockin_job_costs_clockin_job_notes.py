# Generated by Django 4.2.2 on 2023-06-17 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meridian_app', '0002_clockin_duration_clockin_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='clockin',
            name='job_costs',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='clockin',
            name='job_notes',
            field=models.TextField(blank=True),
        ),
    ]
