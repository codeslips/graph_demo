# -*- coding: utf-8 -*-
"""Zhihu platform models."""

from django.db import models

from .base import TimestampMixin


class ZhihuContent(TimestampMixin, models.Model):
    """知乎内容（回答/文章/视频等）。"""

    content_id = models.CharField(max_length=64, db_index=True, help_text="内容ID")
    content_type = models.TextField(blank=True, help_text="内容类型")
    content_text = models.TextField(blank=True, help_text="内容文本")
    content_url = models.TextField(blank=True, help_text="内容URL")
    question_id = models.CharField(max_length=255, blank=True, help_text="问题ID")
    title = models.TextField(blank=True, help_text="标题")
    desc = models.TextField(blank=True, help_text="描述")
    created_time = models.CharField(max_length=32, blank=True, db_index=True, help_text="创建时间")
    updated_time = models.TextField(blank=True, help_text="更新时间")
    voteup_count = models.IntegerField(null=True, blank=True, default=0, help_text="点赞数")
    comment_count = models.IntegerField(null=True, blank=True, default=0, help_text="评论数")
    source_keyword = models.TextField(blank=True, help_text="来源关键词")
    user_id = models.CharField(max_length=255, blank=True, help_text="用户ID")
    user_link = models.TextField(blank=True, help_text="用户链接")
    user_nickname = models.TextField(blank=True, help_text="用户昵称")
    user_avatar = models.TextField(blank=True, help_text="用户头像")
    user_url_token = models.TextField(blank=True, help_text="用户URL Token")

    class Meta:
        db_table = "zhihu_content"
        verbose_name = "知乎内容"
        verbose_name_plural = "知乎内容"

    def __str__(self):
        return f"ZhihuContent({self.content_id})"


class ZhihuComment(TimestampMixin, models.Model):
    """知乎评论。"""

    comment_id = models.CharField(max_length=64, db_index=True, help_text="评论ID")
    parent_comment_id = models.CharField(max_length=64, blank=True, help_text="父评论ID")
    content = models.TextField(blank=True, help_text="评论内容")
    publish_time = models.CharField(max_length=32, blank=True, db_index=True, help_text="发布时间")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    sub_comment_count = models.IntegerField(null=True, blank=True, default=0, help_text="子评论数")
    like_count = models.IntegerField(null=True, blank=True, default=0, help_text="点赞数")
    dislike_count = models.IntegerField(null=True, blank=True, default=0, help_text="踩数")
    content_id = models.CharField(max_length=64, db_index=True, help_text="内容ID")
    content_type = models.TextField(blank=True, help_text="内容类型")
    user_id = models.CharField(max_length=64, blank=True, help_text="用户ID")
    user_link = models.TextField(blank=True, help_text="用户链接")
    user_nickname = models.TextField(blank=True, help_text="用户昵称")
    user_avatar = models.TextField(blank=True, help_text="用户头像")

    class Meta:
        db_table = "zhihu_comment"
        verbose_name = "知乎评论"
        verbose_name_plural = "知乎评论"

    def __str__(self):
        return f"ZhihuComment({self.comment_id})"


class ZhihuCreator(TimestampMixin, models.Model):
    """知乎创作者信息。"""

    user_id = models.CharField(max_length=64, unique=True, db_index=True, help_text="用户ID")
    user_link = models.TextField(blank=True, help_text="用户链接")
    user_nickname = models.TextField(blank=True, help_text="用户昵称")
    user_avatar = models.TextField(blank=True, help_text="用户头像")
    url_token = models.TextField(blank=True, help_text="URL Token")
    gender = models.TextField(blank=True, help_text="性别")
    ip_location = models.TextField(blank=True, help_text="IP归属地")
    follows = models.IntegerField(null=True, blank=True, default=0, help_text="关注数")
    fans = models.IntegerField(null=True, blank=True, default=0, help_text="粉丝数")
    anwser_count = models.IntegerField(null=True, blank=True, default=0, help_text="回答数")
    video_count = models.IntegerField(null=True, blank=True, default=0, help_text="视频数")
    question_count = models.IntegerField(null=True, blank=True, default=0, help_text="提问数")
    article_count = models.IntegerField(null=True, blank=True, default=0, help_text="文章数")
    column_count = models.IntegerField(null=True, blank=True, default=0, help_text="专栏数")
    get_voteup_count = models.IntegerField(null=True, blank=True, default=0, help_text="获赞数")

    class Meta:
        db_table = "zhihu_creator"
        verbose_name = "知乎创作者"
        verbose_name_plural = "知乎创作者"

    def __str__(self):
        return f"ZhihuCreator({self.user_id})"

