# Generated by Django 5.0.3 on 2024-03-27 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitors', '0002_monitor_hour_monitor_minute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='interval',
        ),
    ]
