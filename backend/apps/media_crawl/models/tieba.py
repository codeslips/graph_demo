# -*- coding: utf-8 -*-
"""Tieba platform models."""

from django.db import models

from .base import TimestampMixin


class TiebaNote(TimestampMixin, models.Model):
    """贴吧帖子。"""

    note_id = models.CharField(max_length=644, db_index=True, help_text="帖子ID")
    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")
    note_url = models.TextField(blank=True, help_text="帖子URL")
    publish_time = models.CharField(max_length=255, blank=True, db_index=True, help_text="发布时间")
    user_link = models.TextField(blank=True, default="", help_text="用户链接")
    user_nickname = models.TextField(blank=True, default="", help_text="用户昵称")
    user_avatar = models.TextField(blank=True, default="", help_text="用户头像")
    tieba_id = models.CharField(max_length=255, blank=True, default="", help_text="贴吧ID")
    tieba_name = models.TextField(blank=True, help_text="贴吧名称")
    tieba_link = models.TextField(blank=True, help_text="贴吧链接")
    total_replay_num = models.IntegerField(null=True, blank=True, default=0, help_text="回复数")
    total_replay_page = models.IntegerField(null=True, blank=True, default=0, help_text="回复页数")
    ip_location = models.TextField(blank=True, default="", help_text="IP归属地")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")

    class Meta:
        db_table = "tieba_note"
        verbose_name = "贴吧帖子"
        verbose_name_plural = "贴吧帖子"

    def __str__(self):
        return f"TiebaNote({self.note_id})"


class TiebaComment(TimestampMixin, models.Model):
    """贴吧评论。"""

    comment_id = models.CharField(max_length=255, db_index=True, help_text="评论ID")
    parent_comment_id = models.CharField(max_length=255, blank=True, default="", help_text="父评论ID")
    content = models.TextField(blank=True, help_text="评论内容")
    user_link = models.TextField(blank=True, default="", help_text="用户链接")
    user_nickname = models.TextField(blank=True, default="", help_text="用户昵称")
    user_avatar = models.TextField(blank=True, default="", help_text="用户头像")
    tieba_id = models.CharField(max_length=255, blank=True, default="", help_text="贴吧ID")
    tieba_name = models.TextField(blank=True, help_text="贴吧名称")
    tieba_link = models.TextField(blank=True, help_text="贴吧链接")
    publish_time = models.CharField(max_length=255, blank=True, db_index=True, help_text="发布时间")
    ip_location = models.TextField(blank=True, default="", help_text="IP归属地")
    sub_comment_count = models.IntegerField(null=True, blank=True, default=0, help_text="子评论数")
    note_id = models.CharField(max_length=255, db_index=True, help_text="帖子ID")
    note_url = models.TextField(blank=True, help_text="帖子URL")

    class Meta:
        db_table = "tieba_comment"
        verbose_name = "贴吧评论"
        verbose_name_plural = "贴吧评论"

    def __str__(self):
        return f"TiebaComment({self.comment_id})"


class TiebaCreator(TimestampMixin, models.Model):
    """贴吧创作者信息。"""

    user_id = models.CharField(max_length=64, blank=True, help_text="用户ID")
    user_name = models.TextField(blank=True, help_text="用户名")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    gender = models.TextField(blank=True, help_text="性别")
    follows = models.TextField(blank=True, help_text="关注数")
    fans = models.TextField(blank=True, help_text="粉丝数")
    registration_duration = models.TextField(blank=True, help_text="注册时长")

    class Meta:
        db_table = "tieba_creator"
        verbose_name = "贴吧创作者"
        verbose_name_plural = "贴吧创作者"

    def __str__(self):
        return f"TiebaCreator({self.user_id})"

