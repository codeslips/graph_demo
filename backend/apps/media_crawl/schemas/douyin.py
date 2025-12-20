# -*- coding: utf-8 -*-
"""Douyin platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== DouyinAweme ==============
class DouyinAwemeBase(TimestampMixin):
    """Base schema for DouyinAweme."""

    user_id: Optional[str] = ""
    sec_uid: Optional[str] = ""
    short_user_id: Optional[str] = ""
    user_unique_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    user_signature: Optional[str] = ""
    ip_location: Optional[str] = ""
    aweme_id: int
    aweme_type: Optional[str] = ""
    title: Optional[str] = ""
    desc: Optional[str] = ""
    create_time: Optional[int] = None
    liked_count: Optional[str] = ""
    comment_count: Optional[str] = ""
    share_count: Optional[str] = ""
    collected_count: Optional[str] = ""
    aweme_url: Optional[str] = ""
    cover_url: Optional[str] = ""
    video_download_url: Optional[str] = ""
    music_download_url: Optional[str] = ""
    note_download_url: Optional[str] = ""
    source_keyword: Optional[str] = ""


class DouyinAwemeCreate(DouyinAwemeBase):
    """Schema for creating DouyinAweme."""

    pass


class DouyinAwemeUpdate(Schema):
    """Schema for updating DouyinAweme."""

    user_id: Optional[str] = None
    sec_uid: Optional[str] = None
    short_user_id: Optional[str] = None
    user_unique_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    user_signature: Optional[str] = None
    ip_location: Optional[str] = None
    aweme_type: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    create_time: Optional[int] = None
    liked_count: Optional[str] = None
    comment_count: Optional[str] = None
    share_count: Optional[str] = None
    collected_count: Optional[str] = None
    aweme_url: Optional[str] = None
    cover_url: Optional[str] = None
    video_download_url: Optional[str] = None
    music_download_url: Optional[str] = None
    note_download_url: Optional[str] = None
    source_keyword: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class DouyinAwemeOut(DouyinAwemeBase):
    """Schema for DouyinAweme response."""

    id: int


# ============== DouyinAwemeComment ==============
class DouyinAwemeCommentBase(TimestampMixin):
    """Base schema for DouyinAwemeComment."""

    user_id: Optional[str] = ""
    sec_uid: Optional[str] = ""
    short_user_id: Optional[str] = ""
    user_unique_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    user_signature: Optional[str] = ""
    ip_location: Optional[str] = ""
    comment_id: int
    aweme_id: int
    content: Optional[str] = ""
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = ""
    parent_comment_id: Optional[str] = ""
    like_count: Optional[str] = "0"
    pictures: Optional[str] = ""


class DouyinAwemeCommentCreate(DouyinAwemeCommentBase):
    """Schema for creating DouyinAwemeComment."""

    pass


class DouyinAwemeCommentUpdate(Schema):
    """Schema for updating DouyinAwemeComment."""

    user_id: Optional[str] = None
    sec_uid: Optional[str] = None
    short_user_id: Optional[str] = None
    user_unique_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    user_signature: Optional[str] = None
    ip_location: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = None
    parent_comment_id: Optional[str] = None
    like_count: Optional[str] = None
    pictures: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class DouyinAwemeCommentOut(DouyinAwemeCommentBase):
    """Schema for DouyinAwemeComment response."""

    id: int


# ============== DyCreator ==============
class DyCreatorBase(TimestampMixin):
    """Base schema for DyCreator."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    desc: Optional[str] = ""
    gender: Optional[str] = ""
    follows: Optional[str] = ""
    fans: Optional[str] = ""
    interaction: Optional[str] = ""
    videos_count: Optional[str] = ""


class DyCreatorCreate(DyCreatorBase):
    """Schema for creating DyCreator."""

    pass


class DyCreatorUpdate(Schema):
    """Schema for updating DyCreator."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    desc: Optional[str] = None
    gender: Optional[str] = None
    follows: Optional[str] = None
    fans: Optional[str] = None
    interaction: Optional[str] = None
    videos_count: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class DyCreatorOut(DyCreatorBase):
    """Schema for DyCreator response."""

    id: int

