"""
Coze app configuration.
"""

from django.apps import AppConfig


class CozeConfig(AppConfig):
    """Configuration for the Coze integration app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.coze"
    verbose_name = "Coze AI Chat"

