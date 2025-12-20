# -*- coding: utf-8 -*-
"""Base model classes for media crawl models."""

from django.db import models


class TimestampMixin(models.Model):
    """Mixin for add_ts and last_modify_ts fields."""

    add_ts = models.BigIntegerField(null=True, blank=True, help_text="添加时间戳")
    last_modify_ts = models.BigIntegerField(
        null=True, blank=True, help_text="最后修改时间戳"
    )

    class Meta:
        abstract = True


class UserInfoMixin(models.Model):
    """Mixin for common user info fields."""

    user_id = models.CharField(max_length=255, db_index=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像URL")

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    """Mixin for content fields."""

    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")

    class Meta:
        abstract = True


class CommentMixin(models.Model):
    """Mixin for comment fields."""

    content = models.TextField(blank=True, help_text="评论内容")
    sub_comment_count = models.TextField(blank=True, default="0", help_text="子评论数")
    parent_comment_id = models.CharField(
        max_length=255, blank=True, default="", help_text="父评论ID"
    )
    like_count = models.TextField(blank=True, default="0", help_text="点赞数")

    class Meta:
        abstract = True

