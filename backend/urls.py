from django.contrib import admin
from django.urls import path

from monitors.urls import monitors_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += monitors_urlpatterns