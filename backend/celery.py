import os
import sys

from celery import Celery

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CURRENT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
# Set the timezone

app = Celery("backend")
app.conf.timezone = 'Asia/Dhaka'
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()