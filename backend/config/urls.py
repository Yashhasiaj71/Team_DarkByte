"""
URL Configuration for the Plagiarism Detection project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("detection.urls")),
]
