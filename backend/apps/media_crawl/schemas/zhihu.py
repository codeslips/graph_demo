# -*- coding: utf-8 -*-
"""Zhihu platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== ZhihuContent ==============
class ZhihuContentBase(TimestampMixin):
    """Base schema for ZhihuContent."""

    content_id: str
    content_type: Optional[str] = ""
    content_text: Optional[str] = ""
    content_url: Optional[str] = ""
    question_id: Optional[str] = ""
    title: Optional[str] = ""
    desc: Optional[str] = ""
    created_time: Optional[str] = ""
    updated_time: Optional[str] = ""
    voteup_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    source_keyword: Optional[str] = ""
    user_id: Optional[str] = ""
    user_link: Optional[str] = ""
    user_nickname: Optional[str] = ""
    user_avatar: Optional[str] = ""
    user_url_token: Optional[str] = ""


class ZhihuContentCreate(ZhihuContentBase):
    """Schema for creating ZhihuContent."""

    pass


class ZhihuContentUpdate(Schema):
    """Schema for updating ZhihuContent."""

    content_type: Optional[str] = None
    content_text: Optional[str] = None
    content_url: Optional[str] = None
    question_id: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None
    voteup_count: Optional[int] = None
    comment_count: Optional[int] = None
    source_keyword: Optional[str] = None
    user_id: Optional[str] = None
    user_link: Optional[str] = None
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    user_url_token: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class ZhihuContentOut(ZhihuContentBase):
    """Schema for ZhihuContent response."""

    id: int


# ============== ZhihuComment ==============
class ZhihuCommentBase(TimestampMixin):
    """Base schema for ZhihuComment."""

    comment_id: str
    parent_comment_id: Optional[str] = ""
    content: Optional[str] = ""
    publish_time: Optional[str] = ""
    ip_location: Optional[str] = ""
    sub_comment_count: Optional[int] = 0
    like_count: Optional[int] = 0
    dislike_count: Optional[int] = 0
    content_id: str
    content_type: Optional[str] = ""
    user_id: Optional[str] = ""
    user_link: Optional[str] = ""
    user_nickname: Optional[str] = ""
    user_avatar: Optional[str] = ""


class ZhihuCommentCreate(ZhihuCommentBase):
    """Schema for creating ZhihuComment."""

    pass


class ZhihuCommentUpdate(Schema):
    """Schema for updating ZhihuComment."""

    parent_comment_id: Optional[str] = None
    content: Optional[str] = None
    publish_time: Optional[str] = None
    ip_location: Optional[str] = None
    sub_comment_count: Optional[int] = None
    like_count: Optional[int] = None
    dislike_count: Optional[int] = None
    content_type: Optional[str] = None
    user_id: Optional[str] = None
    user_link: Optional[str] = None
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class ZhihuCommentOut(ZhihuCommentBase):
    """Schema for ZhihuComment response."""

    id: int


# ============== ZhihuCreator ==============
class ZhihuCreatorBase(TimestampMixin):
    """Base schema for ZhihuCreator."""

    user_id: str
    user_link: Optional[str] = ""
    user_nickname: Optional[str] = ""
    user_avatar: Optional[str] = ""
    url_token: Optional[str] = ""
    gender: Optional[str] = ""
    ip_location: Optional[str] = ""
    follows: Optional[int] = 0
    fans: Optional[int] = 0
    anwser_count: Optional[int] = 0
    video_count: Optional[int] = 0
    question_count: Optional[int] = 0
    article_count: Optional[int] = 0
    column_count: Optional[int] = 0
    get_voteup_count: Optional[int] = 0


class ZhihuCreatorCreate(ZhihuCreatorBase):
    """Schema for creating ZhihuCreator."""

    pass


class ZhihuCreatorUpdate(Schema):
    """Schema for updating ZhihuCreator."""

    user_link: Optional[str] = None
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    url_token: Optional[str] = None
    gender: Optional[str] = None
    ip_location: Optional[str] = None
    follows: Optional[int] = None
    fans: Optional[int] = None
    anwser_count: Optional[int] = None
    video_count: Optional[int] = None
    question_count: Optional[int] = None
    article_count: Optional[int] = None
    column_count: Optional[int] = None
    get_voteup_count: Optional[int] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class ZhihuCreatorOut(ZhihuCreatorBase):
    """Schema for ZhihuCreator response."""

    id: int

