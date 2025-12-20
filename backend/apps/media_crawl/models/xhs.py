# -*- coding: utf-8 -*-
"""Xiaohongshu (XHS) platform models."""

from django.db import models

from .base import TimestampMixin


class XhsCreator(TimestampMixin, models.Model):
    """小红书创作者信息。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    desc = models.TextField(blank=True, help_text="个人简介")
    gender = models.TextField(blank=True, help_text="性别")
    follows = models.TextField(blank=True, help_text="关注数")
    fans = models.TextField(blank=True, help_text="粉丝数")
    interaction = models.TextField(blank=True, help_text="互动数")
    tag_list = models.TextField(blank=True, help_text="标签列表")

    class Meta:
        db_table = "xhs_creator"
        verbose_name = "小红书创作者"
        verbose_name_plural = "小红书创作者"

    def __str__(self):
        return f"XhsCreator({self.user_id})"


class XhsNote(TimestampMixin, models.Model):
    """小红书笔记。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    note_id = models.CharField(max_length=255, db_index=True, help_text="笔记ID")
    type = models.TextField(blank=True, help_text="笔记类型")
    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")
    video_url = models.TextField(blank=True, help_text="视频URL")
    time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="发布时间")
    last_update_time = models.BigIntegerField(null=True, blank=True, help_text="最后更新时间")
    liked_count = models.TextField(blank=True, help_text="点赞数")
    collected_count = models.TextField(blank=True, help_text="收藏数")
    comment_count = models.TextField(blank=True, help_text="评论数")
    share_count = models.TextField(blank=True, help_text="分享数")
    image_list = models.TextField(blank=True, help_text="图片列表")
    tag_list = models.TextField(blank=True, help_text="标签列表")
    note_url = models.TextField(blank=True, help_text="笔记URL")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")
    xsec_token = models.TextField(blank=True, help_text="安全令牌")

    class Meta:
        db_table = "xhs_note"
        verbose_name = "小红书笔记"
        verbose_name_plural = "小红书笔记"

    def __str__(self):
        return f"XhsNote({self.note_id})"


class XhsNoteComment(TimestampMixin, models.Model):
    """小红书笔记评论。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    comment_id = models.CharField(max_length=255, db_index=True, help_text="评论ID")
    create_time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="创建时间")
    note_id = models.CharField(max_length=255, blank=True, help_text="笔记ID")
    content = models.TextField(blank=True, help_text="评论内容")
    sub_comment_count = models.IntegerField(null=True, blank=True, help_text="子评论数")
    pictures = models.TextField(blank=True, help_text="图片列表")
    parent_comment_id = models.CharField(max_length=255, blank=True, help_text="父评论ID")
    like_count = models.TextField(blank=True, help_text="点赞数")

    class Meta:
        db_table = "xhs_note_comment"
        verbose_name = "小红书笔记评论"
        verbose_name_plural = "小红书笔记评论"

    def __str__(self):
        return f"XhsNoteComment({self.comment_id})"

