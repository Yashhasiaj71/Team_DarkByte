"""
Database models for the Plagiarism Detection system.

Batch  → a group of uploaded files submitted for comparison
Document → a single file within a batch
Result → pairwise comparison result between two documents
"""

import uuid
from django.db import models
from django.conf import settings


class Batch(models.Model):
    """A batch of files submitted for plagiarism comparison."""

    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    provider = models.CharField(
        max_length=50,
        default="default",
        help_text="Detection provider/algorithm to use",
    )
    options = models.JSONField(
        default=dict,
        blank=True,
        help_text="User-selected detection options (e.g. sensitivity, n-gram size)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "batches"

    def __str__(self):
        return f"Batch {self.id} — {self.status}"


class Document(models.Model):
    """A single uploaded file belonging to a batch."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, related_name="documents"
    )
    original_name = models.CharField(max_length=255)
    minio_key = models.CharField(
        max_length=512, help_text="Object key in MinIO/S3 bucket"
    )
    file_size = models.BigIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, blank=True, default="")
    ai_detection = models.JSONField(
        default=dict,
        blank=True,
        help_text="AI-generated text detection results: score, verdict, features",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

    def __str__(self):
        return self.original_name


class Result(models.Model):
    """Pairwise plagiarism comparison result between two documents."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, related_name="results"
    )
    doc_a = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="results_as_a"
    )
    doc_b = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="results_as_b"
    )
    similarity_pct = models.FloatField(
        help_text="Overall similarity percentage (0.0 – 100.0)"
    )
    details = models.JSONField(
        default=dict,
        help_text="Rich comparison data: fingerprint matches, flagged segments, etc.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-similarity_pct"]

    def __str__(self):
        return (
            f"{self.doc_a.original_name} ↔ {self.doc_b.original_name}: "
            f"{self.similarity_pct:.1f}%"
        )
