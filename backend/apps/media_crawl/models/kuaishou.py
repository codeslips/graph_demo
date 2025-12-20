# -*- coding: utf-8 -*-
"""Kuaishou platform models."""

from django.db import models

from .base import TimestampMixin


class KuaishouVideo(TimestampMixin, models.Model):
    """快手视频。"""

    user_id = models.CharField(max_length=64, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    video_id = models.CharField(max_length=255, db_index=True, help_text="视频ID")
    video_type = models.TextField(blank=True, help_text="视频类型")
    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")
    create_time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="创建时间")
    liked_count = models.TextField(blank=True, help_text="点赞数")
    viewd_count = models.TextField(blank=True, help_text="观看数")
    video_url = models.TextField(blank=True, help_text="视频URL")
    video_cover_url = models.TextField(blank=True, help_text="封面URL")
    video_play_url = models.TextField(blank=True, help_text="播放URL")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")

    class Meta:
        db_table = "kuaishou_video"
        verbose_name = "快手视频"
        verbose_name_plural = "快手视频"

    def __str__(self):
        return f"KuaishouVideo({self.video_id})"


class KuaishouVideoComment(TimestampMixin, models.Model):
    """快手视频评论。"""

    user_id = models.TextField(blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    comment_id = models.BigIntegerField(db_index=True, help_text="评论ID")
    video_id = models.CharField(max_length=255, db_index=True, help_text="视频ID")
    content = models.TextField(blank=True, help_text="评论内容")
    create_time = models.BigIntegerField(null=True, blank=True, help_text="创建时间")
    sub_comment_count = models.TextField(blank=True, help_text="子评论数")

    class Meta:
        db_table = "kuaishou_video_comment"
        verbose_name = "快手视频评论"
        verbose_name_plural = "快手视频评论"

    def __str__(self):
        return f"KuaishouVideoComment({self.comment_id})"

