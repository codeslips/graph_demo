# -*- coding: utf-8 -*-
"""Database router for media_crawl app to use MySQL."""


class MediaCrawlRouter:
    """
    Database router that routes media_crawl app models to MySQL database.
    
    All other apps continue to use the default PostgreSQL database.
    """

    app_label = "media_crawl"
    db_alias = "mysql"

    def db_for_read(self, model, **hints):
        """Route read operations for media_crawl to MySQL."""
        if model._meta.app_label == self.app_label:
            return self.db_alias
        return None

    def db_for_write(self, model, **hints):
        """Route write operations for media_crawl to MySQL."""
        if model._meta.app_label == self.app_label:
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
        """
        if app_label == self.app_label:
            return db == self.db_alias
        return db == "default"

