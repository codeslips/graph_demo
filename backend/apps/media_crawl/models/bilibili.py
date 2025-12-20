# -*- coding: utf-8 -*-
"""Bilibili platform models."""

from django.db import models

from .base import TimestampMixin


class BilibiliVideo(TimestampMixin, models.Model):
    """Bilibili视频信息。"""

    video_id = models.BigIntegerField(unique=True, db_index=True, help_text="视频ID")
    video_url = models.TextField(help_text="视频URL")
    user_id = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="用户昵称")
    avatar = models.TextField(blank=True, help_text="用户头像")
    liked_count = models.IntegerField(null=True, blank=True, help_text="点赞数")
    video_type = models.TextField(blank=True, help_text="视频类型")
    title = models.TextField(blank=True, help_text="视频标题")
    desc = models.TextField(blank=True, help_text="视频描述")
    create_time = models.BigIntegerField(null=True, blank=True, db_index=True, help_text="创建时间")
    disliked_count = models.TextField(blank=True, help_text="踩数")
    video_play_count = models.TextField(blank=True, help_text="播放次数")
    video_favorite_count = models.TextField(blank=True, help_text="收藏数")
    video_share_count = models.TextField(blank=True, help_text="分享数")
    video_coin_count = models.TextField(blank=True, help_text="投币数")
    video_danmaku = models.TextField(blank=True, help_text="弹幕数")
    video_comment = models.TextField(blank=True, help_text="评论数")
    video_cover_url = models.TextField(blank=True, help_text="封面URL")
    source_keyword = models.TextField(blank=True, default="", help_text="来源关键词")

    class Meta:
        db_table = "bilibili_video"
        verbose_name = "Bilibili视频"
        verbose_name_plural = "Bilibili视频"

    def __str__(self):
        return f"BilibiliVideo({self.video_id})"


class BilibiliVideoComment(TimestampMixin, models.Model):
    """Bilibili视频评论。"""

    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="用户昵称")
    sex = models.TextField(blank=True, help_text="性别")
    sign = models.TextField(blank=True, help_text="签名")
    avatar = models.TextField(blank=True, help_text="头像")
    comment_id = models.BigIntegerField(db_index=True, help_text="评论ID")
    video_id = models.BigIntegerField(db_index=True, help_text="视频ID")
    content = models.TextField(blank=True, help_text="评论内容")
    create_time = models.BigIntegerField(null=True, blank=True, help_text="创建时间")
    sub_comment_count = models.TextField(blank=True, help_text="子评论数")
    parent_comment_id = models.CharField(max_length=255, blank=True, help_text="父评论ID")
    like_count = models.TextField(blank=True, default="0", help_text="点赞数")

    class Meta:
        db_table = "bilibili_video_comment"
        verbose_name = "Bilibili视频评论"
        verbose_name_plural = "Bilibili视频评论"

    def __str__(self):
        return f"BilibiliVideoComment({self.comment_id})"


class BilibiliUpInfo(TimestampMixin, models.Model):
    """Bilibili UP主信息。"""

    user_id = models.BigIntegerField(db_index=True, help_text="用户ID")
    nickname = models.TextField(blank=True, help_text="昵称")
    sex = models.TextField(blank=True, help_text="性别")
    sign = models.TextField(blank=True, help_text="签名")
    avatar = models.TextField(blank=True, help_text="头像")
    total_fans = models.IntegerField(null=True, blank=True, help_text="粉丝数")
    total_liked = models.IntegerField(null=True, blank=True, help_text="获赞数")
    user_rank = models.IntegerField(null=True, blank=True, help_text="用户等级")
    is_official = models.IntegerField(null=True, blank=True, help_text="是否官方认证")

    class Meta:
        db_table = "bilibili_up_info"
        verbose_name = "Bilibili UP主信息"
        verbose_name_plural = "Bilibili UP主信息"

    def __str__(self):
        return f"BilibiliUpInfo({self.user_id})"


class BilibiliContactInfo(TimestampMixin, models.Model):
    """Bilibili关注关系。"""

    up_id = models.BigIntegerField(db_index=True, help_text="UP主ID")
    fan_id = models.BigIntegerField(db_index=True, help_text="粉丝ID")
    up_name = models.TextField(blank=True, help_text="UP主名称")
    fan_name = models.TextField(blank=True, help_text="粉丝名称")
    up_sign = models.TextField(blank=True, help_text="UP主签名")
    fan_sign = models.TextField(blank=True, help_text="粉丝签名")
    up_avatar = models.TextField(blank=True, help_text="UP主头像")
    fan_avatar = models.TextField(blank=True, help_text="粉丝头像")

    class Meta:
        db_table = "bilibili_contact_info"
        verbose_name = "Bilibili关注关系"
        verbose_name_plural = "Bilibili关注关系"

    def __str__(self):
        return f"BilibiliContactInfo(up={self.up_id}, fan={self.fan_id})"


class BilibiliUpDynamic(TimestampMixin, models.Model):
    """Bilibili UP主动态。"""

    dynamic_id = models.BigIntegerField(db_index=True, help_text="动态ID")
    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    user_name = models.TextField(blank=True, help_text="用户名")
    text = models.TextField(blank=True, help_text="动态内容")
    type = models.TextField(blank=True, help_text="动态类型")
    pub_ts = models.BigIntegerField(null=True, blank=True, help_text="发布时间戳")
    total_comments = models.IntegerField(null=True, blank=True, help_text="评论数")
    total_forwards = models.IntegerField(null=True, blank=True, help_text="转发数")
    total_liked = models.IntegerField(null=True, blank=True, help_text="点赞数")

    class Meta:
        db_table = "bilibili_up_dynamic"
        verbose_name = "Bilibili UP主动态"
        verbose_name_plural = "Bilibili UP主动态"

    def __str__(self):
        return f"BilibiliUpDynamic({self.dynamic_id})"

