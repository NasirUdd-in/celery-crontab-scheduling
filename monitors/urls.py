from django.urls import re_path
from rest_framework.routers import DefaultRouter

from monitors.views import MonitorRequestViewSet, MonitorViewSet, PeriodicTaskCViewSet

router = DefaultRouter()
router.register(r"monitors", MonitorViewSet)
router.register(r"requests", MonitorRequestViewSet)
router.register(r"periodictask", PeriodicTaskCViewSet)
monitors_urlpatterns = router.urls