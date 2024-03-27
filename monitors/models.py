from django.db import models
from django_celery_beat.models import PeriodicTask


class Monitor(models.Model):

    # monitored endpoint
    endpoint = models.CharField(max_length=1024, blank=False)

    # interval in seconds
    # enpoint will be checked every specified interval time period
    # interval = models.IntegerField(blank=False)
    hour = models.IntegerField(blank=False, default=1)
    minute = models.IntegerField(blank=False, default=30)

    task = models.OneToOneField(
        PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now_add=True)


class MonitorRequest(models.Model):

    # endpoint response time in miliseconds
    response_time = models.IntegerField(blank=False)

    response_status = models.IntegerField(blank=False)

    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
