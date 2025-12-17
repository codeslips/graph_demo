"""
Admin configuration for crawl models.
"""

from django.contrib import admin

from .models import CrawlItem, CrawlTask


@admin.register(CrawlTask)
class CrawlTaskAdmin(admin.ModelAdmin):
    """Admin for CrawlTask model."""

    list_display = [
        "id",
        "crawl_type",
        "status",
        "total_items",
        "created_at",
        "started_at",
        "finished_at",
    ]
    list_filter = ["status", "crawl_type", "created_at"]
    search_fields = ["id", "target_url", "celery_task_id"]
    readonly_fields = [
        "id",
        "created_at",
        "started_at",
        "finished_at",
        "celery_task_id",
    ]
    ordering = ["-created_at"]

    fieldsets = [
        (
            None,
            {
                "fields": ["id", "target_url", "crawl_type", "status"],
            },
        ),
        (
            "Execution",
            {
                "fields": [
                    "total_items",
                    "celery_task_id",
                    "error_message",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "started_at", "finished_at"],
            },
        ),
    ]


@admin.register(CrawlItem)
class CrawlItemAdmin(admin.ModelAdmin):
    """Admin for CrawlItem model."""

    list_display = [
        "cont_id",
        "title_short",
        "channel_name",
        "author",
        "neo4j_synced",
        "created_at",
    ]
    list_filter = ["neo4j_synced", "channel_name", "task"]
    search_fields = ["cont_id", "title", "author"]
    readonly_fields = ["id", "created_at"]
    raw_id_fields = ["task"]
    ordering = ["-created_at"]

    def title_short(self, obj: CrawlItem) -> str:
        """Return truncated title."""
        return obj.title[:60] + "..." if len(obj.title) > 60 else obj.title

    title_short.short_description = "Title"
