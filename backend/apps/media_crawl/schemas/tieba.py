# -*- coding: utf-8 -*-
"""Tieba platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== TiebaNote ==============
class TiebaNoteBase(TimestampMixin):
    """Base schema for TiebaNote."""

    note_id: str
    title: Optional[str] = ""
    desc: Optional[str] = ""
    note_url: Optional[str] = ""
    publish_time: Optional[str] = ""
    user_link: Optional[str] = ""
    user_nickname: Optional[str] = ""
    user_avatar: Optional[str] = ""
    tieba_id: Optional[str] = ""
    tieba_name: Optional[str] = ""
    tieba_link: Optional[str] = ""
    total_replay_num: Optional[int] = 0
    total_replay_page: Optional[int] = 0
    ip_location: Optional[str] = ""
    source_keyword: Optional[str] = ""


class TiebaNoteCreate(TiebaNoteBase):
    """Schema for creating TiebaNote."""

    pass


class TiebaNoteUpdate(Schema):
    """Schema for updating TiebaNote."""

    title: Optional[str] = None
    desc: Optional[str] = None
    note_url: Optional[str] = None
    publish_time: Optional[str] = None
    user_link: Optional[str] = None
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    tieba_id: Optional[str] = None
    tieba_name: Optional[str] = None
    tieba_link: Optional[str] = None
    total_replay_num: Optional[int] = None
    total_replay_page: Optional[int] = None
    ip_location: Optional[str] = None
    source_keyword: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class TiebaNoteOut(TiebaNoteBase):
    """Schema for TiebaNote response."""

    id: int


# ============== TiebaComment ==============
class TiebaCommentBase(TimestampMixin):
    """Base schema for TiebaComment."""

    comment_id: str
    parent_comment_id: Optional[str] = ""
    content: Optional[str] = ""
    user_link: Optional[str] = ""
    user_nickname: Optional[str] = ""
    user_avatar: Optional[str] = ""
    tieba_id: Optional[str] = ""
    tieba_name: Optional[str] = ""
    tieba_link: Optional[str] = ""
    publish_time: Optional[str] = ""
    ip_location: Optional[str] = ""
    sub_comment_count: Optional[int] = 0
    note_id: str
    note_url: Optional[str] = ""


class TiebaCommentCreate(TiebaCommentBase):
    """Schema for creating TiebaComment."""

    pass


class TiebaCommentUpdate(Schema):
    """Schema for updating TiebaComment."""

    parent_comment_id: Optional[str] = None
    content: Optional[str] = None
    user_link: Optional[str] = None
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    tieba_id: Optional[str] = None
    tieba_name: Optional[str] = None
    tieba_link: Optional[str] = None
    publish_time: Optional[str] = None
    ip_location: Optional[str] = None
    sub_comment_count: Optional[int] = None
    note_url: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class TiebaCommentOut(TiebaCommentBase):
    """Schema for TiebaComment response."""

    id: int


# ============== TiebaCreator ==============
class TiebaCreatorBase(TimestampMixin):
    """Base schema for TiebaCreator."""

    user_id: Optional[str] = ""
    user_name: Optional[str] = ""
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    ip_location: Optional[str] = ""
    gender: Optional[str] = ""
    follows: Optional[str] = ""
    fans: Optional[str] = ""
    registration_duration: Optional[str] = ""


class TiebaCreatorCreate(TiebaCreatorBase):
    """Schema for creating TiebaCreator."""

    pass


class TiebaCreatorUpdate(Schema):
    """Schema for updating TiebaCreator."""

    user_id: Optional[str] = None
    user_name: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    ip_location: Optional[str] = None
    gender: Optional[str] = None
    follows: Optional[str] = None
    fans: Optional[str] = None
    registration_duration: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class TiebaCreatorOut(TiebaCreatorBase):
    """Schema for TiebaCreator response."""

    id: int

