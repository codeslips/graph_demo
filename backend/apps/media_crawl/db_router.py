# -*- coding: utf-8 -*-
"""Database router for media_crawl app to use MySQL."""


class MediaCrawlRouter:
    """
    Database router that routes media_crawl app models to MySQL database.
    
    All other apps continue to use the default PostgreSQL database.
    
    Exception: AnalysisReport model uses the default PostgreSQL database.
    """

    app_label = "media_crawl"
    db_alias = "mysql"
    # Models that should use the default PostgreSQL database instead of MySQL
    postgres_models = {"analysisreport"}

    def _is_postgres_model(self, model):
        """Check if the model should use PostgreSQL instead of MySQL."""
        return model._meta.model_name in self.postgres_models

    def db_for_read(self, model, **hints):
        """Route read operations for media_crawl to MySQL (except postgres_models)."""
        if model._meta.app_label == self.app_label:
            if self._is_postgres_model(model):
                return "default"
            return self.db_alias
        return None

    def db_for_write(self, model, **hints):
        """Route write operations for media_crawl to MySQL (except postgres_models)."""
        if model._meta.app_label == self.app_label:
            if self._is_postgres_model(model):
                return "default"
            return self.db_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database.
        
        Prevents cross-database relations between PostgreSQL and MySQL.
        """
        obj1_app = obj1._meta.app_label
        obj2_app = obj2._meta.app_label

        # Both in media_crawl (MySQL)
        if obj1_app == self.app_label and obj2_app == self.app_label:
            return True
        # Both NOT in media_crawl (PostgreSQL)
        if obj1_app != self.app_label and obj2_app != self.app_label:
            return True
        # Cross-database relation - not allowed
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure media_crawl migrations only run on MySQL,
        and other apps only on default (PostgreSQL).
        
        Exception: postgres_models migrate to default database.
        """
        if app_label == self.app_label:
            # AnalysisReport should migrate to default (PostgreSQL)
            if model_name and model_name.lower() in self.postgres_models:
                return db == "default"
            return db == self.db_alias
        return db == "default"

