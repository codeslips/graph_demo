# -*- coding: utf-8 -*-
"""Kuaishou platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== KuaishouVideo ==============
class KuaishouVideoBase(TimestampMixin):
    """Base schema for KuaishouVideo."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    video_id: str
    video_type: Optional[str] = ""
    title: Optional[str] = ""
    desc: Optional[str] = ""
    create_time: Optional[int] = None
    liked_count: Optional[str] = ""
    viewd_count: Optional[str] = ""
    video_url: Optional[str] = ""
    video_cover_url: Optional[str] = ""
    video_play_url: Optional[str] = ""
    source_keyword: Optional[str] = ""


class KuaishouVideoCreate(KuaishouVideoBase):
    """Schema for creating KuaishouVideo."""

    pass


class KuaishouVideoUpdate(Schema):
    """Schema for updating KuaishouVideo."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    video_type: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    create_time: Optional[int] = None
    liked_count: Optional[str] = None
    viewd_count: Optional[str] = None
    video_url: Optional[str] = None
    video_cover_url: Optional[str] = None
    video_play_url: Optional[str] = None
    source_keyword: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class KuaishouVideoOut(KuaishouVideoBase):
    """Schema for KuaishouVideo response."""

    id: int


# ============== KuaishouVideoComment ==============
class KuaishouVideoCommentBase(TimestampMixin):
    """Base schema for KuaishouVideoComment."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    comment_id: int
    video_id: str
    content: Optional[str] = ""
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = ""


class KuaishouVideoCommentCreate(KuaishouVideoCommentBase):
    """Schema for creating KuaishouVideoComment."""

    pass


class KuaishouVideoCommentUpdate(Schema):
    """Schema for updating KuaishouVideoComment."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class KuaishouVideoCommentOut(KuaishouVideoCommentBase):
    """Schema for KuaishouVideoComment response."""

    id: int

