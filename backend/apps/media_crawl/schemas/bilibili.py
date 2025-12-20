# -*- coding: utf-8 -*-
"""Bilibili platform schemas."""

from typing import Optional

from ninja import Schema

from .base import TimestampMixin


# ============== BilibiliVideo ==============
class BilibiliVideoBase(TimestampMixin):
    """Base schema for BilibiliVideo."""

    video_id: int
    video_url: str
    user_id: Optional[int] = None
    nickname: Optional[str] = ""
    avatar: Optional[str] = ""
    liked_count: Optional[int] = None
    video_type: Optional[str] = ""
    title: Optional[str] = ""
    desc: Optional[str] = ""
    create_time: Optional[int] = None
    disliked_count: Optional[str] = ""
    video_play_count: Optional[str] = ""
    video_favorite_count: Optional[str] = ""
    video_share_count: Optional[str] = ""
    video_coin_count: Optional[str] = ""
    video_danmaku: Optional[str] = ""
    video_comment: Optional[str] = ""
    video_cover_url: Optional[str] = ""
    source_keyword: Optional[str] = ""


class BilibiliVideoCreate(BilibiliVideoBase):
    """Schema for creating BilibiliVideo."""

    pass


class BilibiliVideoUpdate(Schema):
    """Schema for updating BilibiliVideo."""

    video_url: Optional[str] = None
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    liked_count: Optional[int] = None
    video_type: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    create_time: Optional[int] = None
    disliked_count: Optional[str] = None
    video_play_count: Optional[str] = None
    video_favorite_count: Optional[str] = None
    video_share_count: Optional[str] = None
    video_coin_count: Optional[str] = None
    video_danmaku: Optional[str] = None
    video_comment: Optional[str] = None
    video_cover_url: Optional[str] = None
    source_keyword: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class BilibiliVideoOut(BilibiliVideoBase):
    """Schema for BilibiliVideo response."""

    id: int


# ============== BilibiliVideoComment ==============
class BilibiliVideoCommentBase(TimestampMixin):
    """Base schema for BilibiliVideoComment."""

    user_id: Optional[str] = ""
    nickname: Optional[str] = ""
    sex: Optional[str] = ""
    sign: Optional[str] = ""
    avatar: Optional[str] = ""
    comment_id: int
    video_id: int
    content: Optional[str] = ""
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = ""
    parent_comment_id: Optional[str] = ""
    like_count: Optional[str] = "0"


class BilibiliVideoCommentCreate(BilibiliVideoCommentBase):
    """Schema for creating BilibiliVideoComment."""

    pass


class BilibiliVideoCommentUpdate(Schema):
    """Schema for updating BilibiliVideoComment."""

    user_id: Optional[str] = None
    nickname: Optional[str] = None
    sex: Optional[str] = None
    sign: Optional[str] = None
    avatar: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[int] = None
    sub_comment_count: Optional[str] = None
    parent_comment_id: Optional[str] = None
    like_count: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class BilibiliVideoCommentOut(BilibiliVideoCommentBase):
    """Schema for BilibiliVideoComment response."""

    id: int


# ============== BilibiliUpInfo ==============
class BilibiliUpInfoBase(TimestampMixin):
    """Base schema for BilibiliUpInfo."""

    user_id: int
    nickname: Optional[str] = ""
    sex: Optional[str] = ""
    sign: Optional[str] = ""
    avatar: Optional[str] = ""
    total_fans: Optional[int] = None
    total_liked: Optional[int] = None
    user_rank: Optional[int] = None
    is_official: Optional[int] = None


class BilibiliUpInfoCreate(BilibiliUpInfoBase):
    """Schema for creating BilibiliUpInfo."""

    pass


class BilibiliUpInfoUpdate(Schema):
    """Schema for updating BilibiliUpInfo."""

    nickname: Optional[str] = None
    sex: Optional[str] = None
    sign: Optional[str] = None
    avatar: Optional[str] = None
    total_fans: Optional[int] = None
    total_liked: Optional[int] = None
    user_rank: Optional[int] = None
    is_official: Optional[int] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class BilibiliUpInfoOut(BilibiliUpInfoBase):
    """Schema for BilibiliUpInfo response."""

    id: int


# ============== BilibiliContactInfo ==============
class BilibiliContactInfoBase(TimestampMixin):
    """Base schema for BilibiliContactInfo."""

    up_id: int
    fan_id: int
    up_name: Optional[str] = ""
    fan_name: Optional[str] = ""
    up_sign: Optional[str] = ""
    fan_sign: Optional[str] = ""
    up_avatar: Optional[str] = ""
    fan_avatar: Optional[str] = ""


class BilibiliContactInfoCreate(BilibiliContactInfoBase):
    """Schema for creating BilibiliContactInfo."""

    pass


class BilibiliContactInfoUpdate(Schema):
    """Schema for updating BilibiliContactInfo."""

    up_name: Optional[str] = None
    fan_name: Optional[str] = None
    up_sign: Optional[str] = None
    fan_sign: Optional[str] = None
    up_avatar: Optional[str] = None
    fan_avatar: Optional[str] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class BilibiliContactInfoOut(BilibiliContactInfoBase):
    """Schema for BilibiliContactInfo response."""

    id: int


# ============== BilibiliUpDynamic ==============
class BilibiliUpDynamicBase(TimestampMixin):
    """Base schema for BilibiliUpDynamic."""

    dynamic_id: int
    user_id: Optional[str] = ""
    user_name: Optional[str] = ""
    text: Optional[str] = ""
    type: Optional[str] = ""
    pub_ts: Optional[int] = None
    total_comments: Optional[int] = None
    total_forwards: Optional[int] = None
    total_liked: Optional[int] = None


class BilibiliUpDynamicCreate(BilibiliUpDynamicBase):
    """Schema for creating BilibiliUpDynamic."""

    pass


class BilibiliUpDynamicUpdate(Schema):
    """Schema for updating BilibiliUpDynamic."""

    user_id: Optional[str] = None
    user_name: Optional[str] = None
    text: Optional[str] = None
    type: Optional[str] = None
    pub_ts: Optional[int] = None
    total_comments: Optional[int] = None
    total_forwards: Optional[int] = None
    total_liked: Optional[int] = None
    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class BilibiliUpDynamicOut(BilibiliUpDynamicBase):
    """Schema for BilibiliUpDynamic response."""

    id: int

