"""
Celery tasks for the detection app.

The main task `process_batch` downloads files from MinIO, runs the
plagiarism detection engine on all pairwise combinations, and stores
results in PostgreSQL.
"""

import logging
from itertools import combinations

import boto3
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Batch, Document, Result
from .engine.text_extractor import extract_text
from .engine.comparator import compare_documents
from .engine.ai_detector import detect_ai

logger = logging.getLogger(__name__)


def _get_s3_client():
    """Create a boto3 S3 client pointed at MinIO."""
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


def _download_file(s3_client, key: str) -> bytes:
    """Download a file from MinIO and return its bytes."""
    response = s3_client.get_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key
    )
    return response["Body"].read()


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def process_batch(self, batch_id: str):
    """
    Process a batch of uploaded documents for plagiarism detection.

    Steps:
    1. Set batch status to 'processing'
    2. Download all documents from MinIO
    3. Extract text from each document
    4. Compare every pair using the detection engine
    5. Store results in PostgreSQL (with JSONB details)
    6. Set batch status to 'completed'
    """
    try:
        batch = Batch.objects.get(id=batch_id)
    except Batch.DoesNotExist:
        logger.error(f"Batch {batch_id} not found")
        return

    # Step 1: Mark as processing
    batch.status = "processing"
    batch.save(update_fields=["status"])

    try:
        s3_client = _get_s3_client()
        documents = list(batch.documents.all())

        if len(documents) < 1:
            logger.warning(f"Batch {batch_id} has no documents, skipping")
            batch.status = "failed"
            batch.save(update_fields=["status"])
            return

        # Step 2 & 3: Download, extract text, and run AI detection
        doc_texts = {}
        for doc in documents:
            logger.info(f"Downloading: {doc.original_name} ({doc.minio_key})")
            file_bytes = _download_file(s3_client, doc.minio_key)
            text = extract_text(file_bytes, doc.original_name)
            doc_texts[doc.id] = text

            # Run AI detection on each document
            logger.info(f"Running AI detection on: {doc.original_name}")
            ai_result = detect_ai(text, use_corpus=True)
            doc.ai_detection = ai_result
            doc.save(update_fields=["ai_detection"])

        # Read comparison options from batch
        options = batch.options or {}
        k = options.get("k_gram_size", 5)
        window_size = options.get("window_size", 4)
        text_weight = options.get("text_weight", 0.4)
        fp_weight = options.get("fingerprint_weight", 0.6)

        if len(documents) == 1:
            # ── Single-file mode: compare against hidden AI reference corpus ──
            _compare_against_corpus(
                batch=batch,
                doc=documents[0],
                doc_text=doc_texts[documents[0].id],
                k=k,
                window_size=window_size,
                text_weight=text_weight,
                fp_weight=fp_weight,
            )
        else:
            # ── Multi-file mode: pairwise comparison ──
            for doc_a, doc_b in combinations(documents, 2):
                logger.info(
                    f"Comparing: {doc_a.original_name} ↔ {doc_b.original_name}"
                )

                result_data = compare_documents(
                    text_a=doc_texts[doc_a.id],
                    text_b=doc_texts[doc_b.id],
                    k=k,
                    window_size=window_size,
                    text_weight=text_weight,
                    fingerprint_weight=fp_weight,
                )

                Result.objects.create(
                    batch=batch,
                    doc_a=doc_a,
                    doc_b=doc_b,
                    similarity_pct=result_data["similarity_pct"],
                    details={
                        "text_similarity": result_data["text_similarity"],
                        "fingerprint_similarity": result_data["fingerprint_similarity"],
                        "matched_fingerprints": result_data["matched_fingerprints"],
                        "total_fingerprints_a": result_data["total_fingerprints_a"],
                        "total_fingerprints_b": result_data["total_fingerprints_b"],
                        "flagged_segments": result_data["flagged_segments"],
                    },
                )

        # Step 6: Mark as completed
        batch.status = "completed"
        batch.completed_at = timezone.now()
        batch.save(update_fields=["status", "completed_at"])
        logger.info(f"Batch {batch_id} completed successfully")

    except Exception as exc:
        logger.exception(f"Batch {batch_id} failed: {exc}")
        batch.status = "failed"
        batch.save(update_fields=["status"])
        # Retry on transient errors
        raise self.retry(exc=exc)


def _compare_against_corpus(batch, doc, doc_text, k, window_size, text_weight, fp_weight):
    """
    Compare a single document against the hidden AI reference corpus.

    Creates hidden Document records (is_reference=True) for each reference
    text and stores comparison results. Reference docs are tagged so the
    frontend can identify single-file mode results.
    """
    from .engine.reference_corpus import get_reference_texts

    ref_corpus = get_reference_texts()

    for ref_id, ref_data in ref_corpus.items():
        logger.info(f"Comparing {doc.original_name} ↔ corpus:{ref_data['title']}")

        # Create a hidden reference Document
        ref_doc = Document.objects.create(
            batch=batch,
            original_name=ref_data["title"],
            minio_key=f"__corpus__/{ref_id}",
            file_size=len(ref_data["text"]),
            mime_type="text/plain",
            ai_detection={"ai_score": 95.0, "verdict": "likely_ai", "features": {}},
        )

        result_data = compare_documents(
            text_a=doc_text,
            text_b=ref_data["text"],
            k=k,
            window_size=window_size,
            text_weight=text_weight,
            fingerprint_weight=fp_weight,
        )

        Result.objects.create(
            batch=batch,
            doc_a=doc,
            doc_b=ref_doc,
            similarity_pct=result_data["similarity_pct"],
            details={
                "text_similarity": result_data["text_similarity"],
                "fingerprint_similarity": result_data["fingerprint_similarity"],
                "matched_fingerprints": result_data["matched_fingerprints"],
                "total_fingerprints_a": result_data["total_fingerprints_a"],
                "total_fingerprints_b": result_data["total_fingerprints_b"],
                "flagged_segments": result_data["flagged_segments"],
                "is_corpus_comparison": True,
            },
        )

