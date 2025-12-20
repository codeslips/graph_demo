# -*- coding: utf-8 -*-
"""Weibo platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== WeiboNote ==============
class WeiboNoteBase(TimestampMixin):
    """Base schema for WeiboNote."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    gender: Optional[str] = ""
    profile_url: Optional[str] = ""
    ip_location: Optional[str] = ""
    note_id: int
    content: Optional[str] = ""
    create_time: Optional[int] = None
    create_date_time: Optional[str] = ""
    liked_count: Optional[str] = ""
    comments_count: Optional[str] = ""
    shared_count: Optional[str] = ""
    note_url: Optional[str] = ""
    source_keyword: Optional[str] = ""


class WeiboNoteCreate(WeiboNoteBase):
    """Schema for creating WeiboNote."""

    pass


class WeiboNoteUpdate(Schema):
    """Schema for updating WeiboNote."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    profile_url: Optional[str] = None
    ip_location: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[int] = None
    create_date_time: Optional[str] = None
    liked_count: Optional[str] = None
    comments_count: Optional[str] = None
    shared_count: Optional[str] = None
    note_url: Optional[str] = None
    source_keyword: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class WeiboNoteOut(WeiboNoteBase):
    """Schema for WeiboNote response."""

    id: int


# ============== WeiboNoteComment ==============
class WeiboNoteCommentBase(TimestampMixin):
    """Base schema for WeiboNoteComment."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    gender: Optional[str] = ""
    profile_url: Optional[str] = ""
    ip_location: Optional[str] = ""
    comment_id: int
    note_id: int
    content: Optional[str] = ""
    create_time: Optional[int] = None
    create_date_time: Optional[str] = ""
    comment_like_count: Optional[str] = ""
    sub_comment_count: Optional[str] = ""
    parent_comment_id: Optional[str] = ""


class WeiboNoteCommentCreate(WeiboNoteCommentBase):
    """Schema for creating WeiboNoteComment."""

    pass


class WeiboNoteCommentUpdate(Schema):
    """Schema for updating WeiboNoteComment."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    profile_url: Optional[str] = None
    ip_location: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[int] = None
    create_date_time: Optional[str] = None
    comment_like_count: Optional[str] = None
    sub_comment_count: Optional[str] = None
    parent_comment_id: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class WeiboNoteCommentOut(WeiboNoteCommentBase):
    """Schema for WeiboNoteComment response."""

    id: int


# ============== WeiboCreator ==============
class WeiboCreatorBase(TimestampMixin):
    """Base schema for WeiboCreator."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    desc: Optional[str] = ""
    gender: Optional[str] = ""
    follows: Optional[str] = ""
    fans: Optional[str] = ""
    tag_list: Optional[str] = ""


class WeiboCreatorCreate(WeiboCreatorBase):
    """Schema for creating WeiboCreator."""

    pass


class WeiboCreatorUpdate(Schema):
    """Schema for updating WeiboCreator."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    desc: Optional[str] = None
    gender: Optional[str] = None
    follows: Optional[str] = None
    fans: Optional[str] = None
    tag_list: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class WeiboCreatorOut(WeiboCreatorBase):
    """Schema for WeiboCreator response."""

    id: int

