"""
DRF serializers for the detection app.
"""

from rest_framework import serializers
from .models import Batch, Document, Result


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "original_name",
            "minio_key",
            "file_size",
            "mime_type",
            "ai_detection",
            "uploaded_at",
        ]
        read_only_fields = fields


class ResultSerializer(serializers.ModelSerializer):
    doc_a_name = serializers.CharField(source="doc_a.original_name", read_only=True)
    doc_b_name = serializers.CharField(source="doc_b.original_name", read_only=True)

    class Meta:
        model = Result
        fields = [
            "id",
            "doc_a",
            "doc_a_name",
            "doc_b",
            "doc_b_name",
            "similarity_pct",
            "details",
            "created_at",
        ]
        read_only_fields = fields


class BatchListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing batches."""

    document_count = serializers.IntegerField(
        source="documents.count", read_only=True
    )

    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "status",
            "provider",
            "options",
            "document_count",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["id", "status", "created_at", "completed_at"]


class BatchDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested documents and results for polling."""

    documents = DocumentSerializer(many=True, read_only=True)
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "status",
            "provider",
            "options",
            "documents",
            "results",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields
