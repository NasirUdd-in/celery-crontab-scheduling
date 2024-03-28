import json

from django.db import transaction
from django.shortcuts import render
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from monitors.models import Monitor, MonitorRequest
from monitors.serializers import MonitorRequestSerializer, MonitorSerializer

import zoneinfo

# from rest_framework.exceptions import ValidationError


class MonitorViewSet(viewsets.ModelViewSet):

    serializer_class = MonitorSerializer
    queryset = Monitor.objects.all()

    def perform_create(self, serializer):
        try:
            # instance = serializer.validated_data

            # Ensure hour is within the specified range (12 to 24)
            # if instance['hour'] < 12 or instance['hour'] > 24:
            #     raise ValidationError("Hour must be between 12 and 24.")
            
            with transaction.atomic():

                instance = serializer.save()
                # if instance.hour < 12 or instance.hour > 24:
                #     raise ValidationError("Hour must be between 12 and 24.")
                
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    hour=instance.hour,
                    minute=instance.minute,
                    day_of_week='*',
                    day_of_month='*',
                    month_of_year='*',
                    timezone=zoneinfo.ZoneInfo('Asia/Dhaka')
                )

                task = PeriodicTask.objects.create(
                    crontab=schedule,
                    name=f"Monitor: {instance.endpoint}",
                    task="monitors.tasks.task_monitor",
                    kwargs=json.dumps(
                        {
                            "monitor_id": instance.id,
                        }
                    ),
                )
                instance.task = task
                instance.save()

        except Exception as e:
            raise APIException(str(e))

    def perform_destroy(self, instance):
        if instance.task is not None:
            instance.task.delete()
        return super().perform_destroy(instance)
    
    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                # Assuming you want to update interval for a specific name
                task_name = f"Monitor: {instance.endpoint}"
                task = PeriodicTask.objects.filter(name=task_name).first()
                if task:
                    schedule, _ = CrontabSchedule.objects.get_or_create(
                        hour=instance.hour,
                        minute=instance.minute,
                        day_of_week='*',
                        day_of_month='*',
                        month_of_year='*',
                        timezone=zoneinfo.ZoneInfo('Asia/Dhaka')
                    )
                    task.crontab = schedule
                    task.save()
        except Exception as e:
            raise APIException(str(e))


class MonitorRequestViewSet(viewsets.ModelViewSet):

    serializer_class = MonitorRequestSerializer
    queryset = MonitorRequest.objects.all()
