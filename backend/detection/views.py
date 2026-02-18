"""
API views for the detection app.

- BatchListCreateView: POST to upload files + create batch, GET to list batches
- BatchDetailView: GET to poll status + results, DELETE to remove a batch
"""

import uuid
import boto3
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Batch, Document
from .serializers import BatchListSerializer, BatchDetailSerializer


def get_s3_client():
    """Create a boto3 S3 client pointed at MinIO."""
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


def ensure_bucket_exists(s3_client, bucket_name):
    """Create the MinIO bucket if it doesn't exist."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)


class BatchListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/batches/       → List all batches
    POST /api/batches/       → Upload files + create a new batch
    """

    queryset = Batch.objects.all()
    serializer_class = BatchListSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist("files")
        if not files:
            return Response(
                {"error": "No files provided. Upload at least 1 file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the batch record
        batch = Batch.objects.create(
            name=request.data.get("name", ""),
            provider=request.data.get("provider", "default"),
            options=self._parse_options(request.data.get("options", "{}")),
        )

        # Upload files to MinIO and create Document records
        s3_client = get_s3_client()
        ensure_bucket_exists(s3_client, settings.AWS_STORAGE_BUCKET_NAME)

        for f in files:
            object_key = f"{batch.id}/{uuid.uuid4()}/{f.name}"
            s3_client.upload_fileobj(
                f, settings.AWS_STORAGE_BUCKET_NAME, object_key
            )

            Document.objects.create(
                batch=batch,
                original_name=f.name,
                minio_key=object_key,
                file_size=f.size,
                mime_type=f.content_type or "",
            )

        # Dispatch the Celery background task
        from .tasks import process_batch

        process_batch.delay(str(batch.id))

        serializer = BatchDetailSerializer(batch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _parse_options(self, options_raw):
        """Safely parse options JSON from the request."""
        import json

        if isinstance(options_raw, dict):
            return options_raw
        try:
            return json.loads(options_raw)
        except (json.JSONDecodeError, TypeError):
            return {}


class BatchDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/batches/<id>/  → Poll batch status + results
    DELETE /api/batches/<id>/  → Delete a batch and its files
    """

    queryset = Batch.objects.all()
    serializer_class = BatchDetailSerializer

    def perform_destroy(self, instance):
        """Also clean up files from MinIO when deleting a batch."""
        s3_client = get_s3_client()
        for doc in instance.documents.all():
            try:
                s3_client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=doc.minio_key
                )
            except Exception:
                pass  # best-effort cleanup
        instance.delete()


class TextBatchCreateView(generics.CreateAPIView):
    """
    POST /api/batches/text/  → Create a batch from named text entries.

    Accepts JSON body:
    {
      "name": "Batch name",
      "entries": [
        { "author": "Student A", "text": "Their essay text..." },
        { "author": "Student B", "text": "Their essay text..." }
      ],
      "options": { "k_gram_size": 5, "window_size": 4 }
    }
    """

    serializer_class = BatchDetailSerializer
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        entries = request.data.get("entries", [])
        if len(entries) < 2:
            return Response(
                {"error": "At least 2 text entries are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate entries
        for i, entry in enumerate(entries):
            if not entry.get("author", "").strip():
                return Response(
                    {"error": f"Entry {i + 1} is missing an author name."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not entry.get("text", "").strip():
                return Response(
                    {"error": f"Entry {i + 1} ({entry.get('author', '')}) has no text."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Parse options
        options_raw = request.data.get("options", {})
        if isinstance(options_raw, str):
            import json
            try:
                options_raw = json.loads(options_raw)
            except (json.JSONDecodeError, TypeError):
                options_raw = {}

        # Create the batch
        batch = Batch.objects.create(
            name=request.data.get("name", "Text Comparison"),
            provider=request.data.get("provider", "default"),
            options=options_raw,
        )

        # Upload each text entry to MinIO and create Document records
        s3_client = get_s3_client()
        ensure_bucket_exists(s3_client, settings.AWS_STORAGE_BUCKET_NAME)

        for entry in entries:
            author = entry["author"].strip()
            text = entry["text"].strip()
            text_bytes = text.encode("utf-8")

            object_key = f"{batch.id}/{uuid.uuid4()}/{author}.txt"
            import io
            s3_client.upload_fileobj(
                io.BytesIO(text_bytes),
                settings.AWS_STORAGE_BUCKET_NAME,
                object_key,
            )

            Document.objects.create(
                batch=batch,
                original_name=author,
                minio_key=object_key,
                file_size=len(text_bytes),
                mime_type="text/plain",
            )

        # Dispatch the Celery task
        from .tasks import process_batch
        process_batch.delay(str(batch.id))

        serializer = BatchDetailSerializer(batch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
