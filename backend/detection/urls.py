"""
URL routing for the detection app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("batches/", views.BatchListCreateView.as_view(), name="batch-list-create"),
    path("batches/text/", views.TextBatchCreateView.as_view(), name="batch-text-create"),
    path("batches/<uuid:pk>/", views.BatchDetailView.as_view(), name="batch-detail"),
]
