# -*- coding: utf-8 -*-
"""Weibo platform models."""

from django.db import models

from .base import TimestampMixin


class WeiboNote(TimestampMixin, models.Model):
    """微博帖子。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    gender = models.TextField(blank=True, help_text="性别")
    profile_url = models.TextField(blank=True, help_text="主页URL")
    ip_location = models.TextField(blank=True, default="", help_text="IP归属地")
    note_id = models.BigIntegerField(db_index=True, help_text="帖子ID")
    content = models.TextField(blank=True, help_text="内容")
    create_time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="创建时间戳")
    create_date_time = models.CharField(max_length=255, blank=True, db_index=True, help_text="创建时间字符串")
    liked_count = models.TextField(blank=True, help_text="点赞数")
    comments_count = models.TextField(blank=True, help_text="评论数")
    shared_count = models.TextField(blank=True, help_text="转发数")
    note_url = models.TextField(blank=True, help_text="帖子URL")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")

    class Meta:
        db_table = "weibo_note"
        verbose_name = "微博帖子"
        verbose_name_plural = "微博帖子"

    def __str__(self):
        return f"WeiboNote({self.note_id})"


class WeiboNoteComment(TimestampMixin, models.Model):
    """微博帖子评论。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    gender = models.TextField(blank=True, help_text="性别")
    profile_url = models.TextField(blank=True, help_text="主页URL")
    ip_location = models.TextField(blank=True, default="", help_text="IP归属地")
    comment_id = models.BigIntegerField(db_index=True, help_text="评论ID")
    note_id = models.BigIntegerField(db_index=True, help_text="帖子ID")
    content = models.TextField(blank=True, help_text="评论内容")
    create_time = models.BigIntegerField(null=True, blank=True, help_text="创建时间戳")
    create_date_time = models.CharField(max_length=255, blank=True, db_index=True, help_text="创建时间字符串")
    comment_like_count = models.TextField(blank=True, help_text="评论点赞数")
    sub_comment_count = models.TextField(blank=True, help_text="子评论数")
    parent_comment_id = models.CharField(max_length=255, blank=True, help_text="父评论ID")

    class Meta:
        db_table = "weibo_note_comment"
        verbose_name = "微博帖子评论"
        verbose_name_plural = "微博帖子评论"

    def __str__(self):
        return f"WeiboNoteComment({self.comment_id})"


class WeiboCreator(TimestampMixin, models.Model):
    """微博创作者信息。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    desc = models.TextField(blank=True, help_text="个人简介")
    gender = models.TextField(blank=True, help_text="性别")
    follows = models.TextField(blank=True, help_text="关注数")
    fans = models.TextField(blank=True, help_text="粉丝数")
    tag_list = models.TextField(blank=True, help_text="标签列表")

    class Meta:
        db_table = "weibo_creator"
        verbose_name = "微博创作者"
        verbose_name_plural = "微博创作者"

    def __str__(self):
        return f"WeiboCreator({self.user_id})"

