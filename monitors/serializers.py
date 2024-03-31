from rest_framework import serializers

from monitors.models import Monitor, MonitorRequest

from django_celery_beat.models import PeriodicTask

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        read_only_fields = ("id", "created_at")
        fields = (
            "id",
            "created_at",
            "endpoint",
            "hour",
            "minute"
        )


class MonitorRequestSerializer(serializers.ModelSerializer):
    monitor_endpoint = serializers.SerializerMethodField()

    def get_monitor_endpoint(self, obj):
        return obj.monitor.endpoint

    class Meta:
        model = MonitorRequest
        read_only_fields = ("id", "created_at")
        fields = (
            "id",
            "created_at",
            "response_time",
            "response_status",
            "monitor_endpoint",
        )

class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = (
            "name",
            "enabled"
        )