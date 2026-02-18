from django.contrib import admin
from .models import Batch, Document, Result


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ("id", "minio_key", "file_size", "uploaded_at")


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    readonly_fields = ("id", "doc_a", "doc_b", "similarity_pct", "created_at")


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "provider", "created_at", "completed_at")
    list_filter = ("status", "provider")
    search_fields = ("name",)
    inlines = [DocumentInline, ResultInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "original_name", "batch", "file_size", "uploaded_at")
    list_filter = ("batch",)
    search_fields = ("original_name",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "batch", "doc_a", "doc_b", "similarity_pct", "created_at")
    list_filter = ("batch",)
