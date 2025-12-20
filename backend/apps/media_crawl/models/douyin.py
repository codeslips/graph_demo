# -*- coding: utf-8 -*-
"""Douyin platform models."""

from django.db import models

from .base import TimestampMixin


class DouyinAweme(TimestampMixin, models.Model):
    """抖音视频/作品。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    sec_uid = models.CharField(max_length=255, blank=True, help_text="加密用户ID")
    short_user_id = models.CharField(max_length=255, blank=True, help_text="短用户ID")
    user_unique_id = models.CharField(max_length=255, blank=True, help_text="唯一用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    user_signature = models.TextField(blank=True, help_text="用户签名")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    aweme_id = models.BigIntegerField(db_index=True, help_text="作品ID")
    aweme_type = models.TextField(blank=True, help_text="作品类型")
    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")
    create_time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="创建时间")
    liked_count = models.TextField(blank=True, help_text="点赞数")
    comment_count = models.TextField(blank=True, help_text="评论数")
    share_count = models.TextField(blank=True, help_text="分享数")
    collected_count = models.TextField(blank=True, help_text="收藏数")
    aweme_url = models.TextField(blank=True, help_text="作品URL")
    cover_url = models.TextField(blank=True, help_text="封面URL")
    video_download_url = models.TextField(blank=True, help_text="视频下载URL")
    music_download_url = models.TextField(blank=True, help_text="音乐下载URL")
    note_download_url = models.TextField(blank=True, help_text="笔记下载URL")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")

    class Meta:
        db_table = "douyin_aweme"
        verbose_name = "抖音作品"
        verbose_name_plural = "抖音作品"

    def __str__(self):
        return f"DouyinAweme({self.aweme_id})"


class DouyinAwemeComment(TimestampMixin, models.Model):
    """抖音作品评论。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    sec_uid = models.CharField(max_length=255, blank=True, help_text="加密用户ID")
    short_user_id = models.CharField(max_length=255, blank=True, help_text="短用户ID")
    user_unique_id = models.CharField(max_length=255, blank=True, help_text="唯一用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    user_signature = models.TextField(blank=True, help_text="用户签名")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    comment_id = models.BigIntegerField(db_index=True, help_text="评论ID")
    aweme_id = models.BigIntegerField(db_index=True, help_text="作品ID")
    content = models.TextField(blank=True, help_text="评论内容")
    create_time = models.BigIntegerField(null=True, blank=True, help_text="创建时间")
    sub_comment_count = models.TextField(blank=True, help_text="子评论数")
    parent_comment_id = models.CharField(max_length=255, blank=True, help_text="父评论ID")
    like_count = models.TextField(blank=True, default="0", help_text="点赞数")
    pictures = models.TextField(blank=True, default="", help_text="图片列表")

    class Meta:
        db_table = "douyin_aweme_comment"
        verbose_name = "抖音作品评论"
        verbose_name_plural = "抖音作品评论"

    def __str__(self):
        return f"DouyinAwemeComment({self.comment_id})"


class DyCreator(TimestampMixin, models.Model):
    """抖音创作者信息。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    avatar = models.TextField(blank=True, help_text="头像")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    desc = models.TextField(blank=True, help_text="个人简介")
    gender = models.TextField(blank=True, help_text="性别")
    follows = models.TextField(blank=True, help_text="关注数")
    fans = models.TextField(blank=True, help_text="粉丝数")
    interaction = models.TextField(blank=True, help_text="互动数")
    videos_count = models.CharField(max_length=255, blank=True, help_text="作品数")

    class Meta:
        db_table = "dy_creator"
        verbose_name = "抖音创作者"
        verbose_name_plural = "抖音创作者"

    def __str__(self):
        return f"DyCreator({self.user_id})"

