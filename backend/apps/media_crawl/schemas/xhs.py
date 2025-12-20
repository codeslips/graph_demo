# -*- coding: utf-8 -*-
"""Xiaohongshu (XHS) platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== XhsCreator ==============
class XhsCreatorBase(TimestampMixin):
    """Base schema for XhsCreator."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    desc: Optional[str] = ""
    gender: Optional[str] = ""
    follows: Optional[str] = ""
    fans: Optional[str] = ""
    interaction: Optional[str] = ""
    tag_list: Optional[str] = ""


class XhsCreatorCreate(XhsCreatorBase):
    """Schema for creating XhsCreator."""

    pass


class XhsCreatorUpdate(Schema):
    """Schema for updating XhsCreator."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    desc: Optional[str] = None
    gender: Optional[str] = None
    follows: Optional[str] = None
    fans: Optional[str] = None
    interaction: Optional[str] = None
    tag_list: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class XhsCreatorOut(XhsCreatorBase):
    """Schema for XhsCreator response."""

    id: int


# ============== XhsNote ==============
class XhsNoteBase(TimestampMixin):
    """Base schema for XhsNote."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    note_id: str
    type: Optional[str] = ""
    title: Optional[str] = ""
    desc: Optional[str] = ""
    video_url: Optional[str] = ""
    time: Optional[int] = None
    last_update_time: Optional[int] = None
    liked_count: Optional[str] = ""
    collected_count: Optional[str] = ""
    comment_count: Optional[str] = ""
    share_count: Optional[str] = ""
    image_list: Optional[str] = ""
    tag_list: Optional[str] = ""
    note_url: Optional[str] = ""
    source_keyword: Optional[str] = ""
    xsec_token: Optional[str] = ""


class XhsNoteCreate(XhsNoteBase):
    """Schema for creating XhsNote."""

    pass


class XhsNoteUpdate(Schema):
    """Schema for updating XhsNote."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    video_url: Optional[str] = None
    time: Optional[int] = None
    last_update_time: Optional[int] = None
    liked_count: Optional[str] = None
    collected_count: Optional[str] = None
    comment_count: Optional[str] = None
    share_count: Optional[str] = None
    image_list: Optional[str] = None
    tag_list: Optional[str] = None
    note_url: Optional[str] = None
    source_keyword: Optional[str] = None
    xsec_token: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class XhsNoteOut(XhsNoteBase):
    """Schema for XhsNote response."""

    id: int


# ============== XhsNoteComment ==============
class XhsNoteCommentBase(TimestampMixin):
    """Base schema for XhsNoteComment."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    comment_id: str
    create_time: Optional[int] = None
    note_id: Optional[str] = ""
    content: Optional[str] = ""
    sub_comment_count: Optional[int] = None
    pictures: Optional[str] = ""
    parent_comment_id: Optional[str] = ""
    like_count: Optional[str] = ""


class XhsNoteCommentCreate(XhsNoteCommentBase):
    """Schema for creating XhsNoteComment."""

    pass


class XhsNoteCommentUpdate(Schema):
    """Schema for updating XhsNoteComment."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    create_time: Optional[int] = None
    note_id: Optional[str] = None
    content: Optional[str] = None
    sub_comment_count: Optional[int] = None
    pictures: Optional[str] = None
    parent_comment_id: Optional[str] = None
    like_count: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class XhsNoteCommentOut(XhsNoteCommentBase):
    """Schema for XhsNoteComment response."""

    id: int

