# -*- coding: utf-8 -*-
"""Bilibili API endpoints."""

from ninja import Router

from ..models import (
    BilibiliContactInfo,
    BilibiliUpDynamic,
    BilibiliUpInfo,
    BilibiliVideo,
    BilibiliVideoComment,
)
from ..schemas.bilibili import (
    BilibiliContactInfoCreate,
    BilibiliContactInfoOut,
    BilibiliContactInfoUpdate,
    BilibiliUpDynamicCreate,
    BilibiliUpDynamicOut,
    BilibiliUpDynamicUpdate,
    BilibiliUpInfoCreate,
    BilibiliUpInfoOut,
    BilibiliUpInfoUpdate,
    BilibiliVideoCommentCreate,
    BilibiliVideoCommentOut,
    BilibiliVideoCommentUpdate,
    BilibiliVideoCreate,
    BilibiliVideoOut,
    BilibiliVideoUpdate,
)
from .base import create_crud_router

# Create routers for each model
videos_router = create_crud_router(
    model=BilibiliVideo,
    create_schema=BilibiliVideoCreate,
    update_schema=BilibiliVideoUpdate,
    out_schema=BilibiliVideoOut,
    tags=["Bilibili - Videos"],
    time_field="create_time",
)

comments_router = create_crud_router(
    model=BilibiliVideoComment,
    create_schema=BilibiliVideoCommentCreate,
    update_schema=BilibiliVideoCommentUpdate,
    out_schema=BilibiliVideoCommentOut,
    tags=["Bilibili - Comments"],
    time_field="create_time",
)

ups_router = create_crud_router(
    model=BilibiliUpInfo,
    create_schema=BilibiliUpInfoCreate,
    update_schema=BilibiliUpInfoUpdate,
    out_schema=BilibiliUpInfoOut,
    tags=["Bilibili - UP Info"],
    time_field=None,
)

contacts_router = create_crud_router(
    model=BilibiliContactInfo,
    create_schema=BilibiliContactInfoCreate,
    update_schema=BilibiliContactInfoUpdate,
    out_schema=BilibiliContactInfoOut,
    tags=["Bilibili - Contacts"],
    time_field=None,
)

dynamics_router = create_crud_router(
    model=BilibiliUpDynamic,
    create_schema=BilibiliUpDynamicCreate,
    update_schema=BilibiliUpDynamicUpdate,
    out_schema=BilibiliUpDynamicOut,
    tags=["Bilibili - Dynamics"],
    time_field="pub_ts",
)

# Main Bilibili router
router = Router(tags=["Bilibili"])
router.add_router("/videos", videos_router)
router.add_router("/comments", comments_router)
router.add_router("/ups", ups_router)
router.add_router("/contacts", contacts_router)
router.add_router("/dynamics", dynamics_router)

